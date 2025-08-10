from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import mysql.connector
from flask_mail import Message
from extensions import app, mail, get_db_connection
import random
import re
from functools import wraps
import json
from user_agents import parse
from flask import current_app

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Add parse_user_agent to template globals
def parse_user_agent(ua_string):
    ua = parse(ua_string)
    return {
        'browser': f"{ua.browser.family} {ua.browser.version_string}",
        'os': f"{ua.os.family} {ua.os.version_string}"
    }

# Register the function in template globals
admin_bp.add_app_template_global(parse_user_agent, 'parse_user_agent')

def parse_user_agent_safe(ua_string):
    if not ua_string:
        return {'browser': 'Unknown', 'os': 'Unknown'}
    
    try:
        ua = parse(ua_string)
        browser = f"{ua.browser.family} {ua.browser.version_string}".strip() if ua.browser else 'Unknown Browser'
        os = f"{ua.os.family} {ua.os.version_string}".strip() if ua.os else 'Unknown OS'
        return {
            'browser': browser,
            'os': os
        }
    except Exception:
        return {'browser': 'Unknown', 'os': 'Unknown'}
    
def log_admin_action(action, details=None):
    if 'admin_id' in session:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            user_agent = request.headers.get('User-Agent')
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            
            cursor.execute("""
                INSERT INTO admin_logs (admin_id, action, details, ip_address, user_agent)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                session['admin_id'],
                action,
                json.dumps(details) if details else None,
                ip_address,
                str(user_agent)
            ))
            conn.commit()
            
# Admin login required decorator
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in as admin to access this page', 'danger')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Superadmin required decorator
def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in as admin to access this page', 'danger')
            return redirect(url_for('admin.admin_login'))
        
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT is_superadmin FROM admins WHERE id = %s", (session['admin_id'],))
            admin = cursor.fetchone()
            
            if not admin or not admin['is_superadmin']:
                flash('You need superadmin privileges to access this page', 'danger')
                return redirect(url_for('admin.admin_dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

# Log admin action
def log_admin_action(action, details=None):
    if 'admin_id' in session:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            user_agent = parse(request.headers.get('User-Agent'))
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            
            cursor.execute("""
                INSERT INTO admin_logs (admin_id, action, details, ip_address, user_agent)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                session['admin_id'],
                action,
                json.dumps(details) if details else None,
                ip_address,
                str(user_agent)
            ))
            conn.commit()

# Admin login - updated to redirect to login_as if coming from there
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # Check if coming from login_as page
    if request.referrer and 'login_as' in request.referrer and request.method == 'GET':
        session['from_login_as'] = True
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            admin = cursor.fetchone()
            
            if admin and check_password_hash(admin['password'], password):
                session['admin_id'] = admin['id']
                session['admin_name'] = admin['full_name']
                session['is_superadmin'] = admin['is_superadmin']
                
                # Update last login
                cursor.execute("UPDATE admins SET last_login = NOW() WHERE id = %s", (admin['id'],))
                conn.commit()
                
                # Log login
                log_admin_action("Admin Login")
                
                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('Invalid username or password', 'danger')
    
    # If coming from login_as, show a slightly different template
    if session.get('from_login_as'):
        session.pop('from_login_as')
        return render_template('admin/admin_login.html', from_login_as=True)
    
    return render_template('admin/admin_login.html')


# View report details
@admin_bp.route('/view_report/<int:report_id>')
@admin_login_required
def view_report(report_id):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get report with user and admin info
        cursor.execute("""
            SELECT 
                cr.*, 
                u.fname, u.lname, u.email, u.phone_num,
                a.full_name as admin_name
            FROM crime_reports cr
            JOIN users u ON cr.user_id = u.id
            LEFT JOIN admins a ON cr.admin_id = a.id
            WHERE cr.id = %s
        """, (report_id,))
        report = cursor.fetchone()
        
        if not report:
            flash('Report not found', 'danger')
            return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin/admin_view.html', report=report)

# Update report status (modified version)
@admin_bp.route('/update_report_status/<int:report_id>', methods=['POST'])
@admin_login_required
def update_report_status(report_id):
    status = request.form['status']
    feedback = request.form.get('feedback', '')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE crime_reports 
            SET 
                status = %s, 
                admin_feedback = %s, 
                admin_id = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (status, feedback, session['admin_id'], report_id))
        conn.commit()
        
        # Get report details for logging
        cursor.execute("""
            SELECT cr.*, u.fname, u.lname, u.email
            FROM crime_reports cr
            JOIN users u ON cr.user_id = u.id
            WHERE cr.id = %s
        """, (report_id,))
        report = cursor.fetchone()
        
        log_admin_action("Update Report Status", {
            'report_id': report_id,
            'status': status,
            'feedback': feedback[:100]  # Log first 100 chars of feedback
        })
    
    flash('Report status updated successfully', 'success')
    return redirect(url_for('admin.view_report', report_id=report_id))

# Admin dashboard
@admin_bp.route('/dashboard')
@admin_login_required
def admin_dashboard():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get all reports with user info (updated query)
        cursor.execute("""
            SELECT 
                cr.*, 
                u.fname, u.lname, u.email, u.phone_num,
                a.full_name as admin_name
            FROM crime_reports cr
            JOIN users u ON cr.user_id = u.id
            LEFT JOIN admins a ON cr.admin_id = a.id
            ORDER BY cr.report_date DESC
            LIMIT 50
        """)
        reports = cursor.fetchall()
        
        
        # Get stats for dashboard
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        cursor.execute("SELECT COUNT(*) as total_reports FROM crime_reports")
        total_reports = cursor.fetchone()['total_reports']
        
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM crime_reports 
            GROUP BY status
        """)
        status_data = cursor.fetchall()
        
        cursor.execute("""
            SELECT incident_type, COUNT(*) as count 
            FROM crime_reports 
            GROUP BY incident_type
            ORDER BY count DESC
            LIMIT 5
        """)
        top_crimes = cursor.fetchall()
        
        cursor.execute("""
            SELECT location, COUNT(*) as count 
            FROM crime_reports 
            GROUP BY location 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_locations = cursor.fetchall()
    
    return render_template('admin/admin_dashboard.html', 
                         reports=reports,
                         total_users=total_users,
                         total_reports=total_reports,
                         status_data=status_data,
                         top_crimes=top_crimes,
                         top_locations=top_locations)



# Admin analysis
@admin_bp.route('/analysis')
@admin_login_required
def admin_analysis():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Crime type distribution
        cursor.execute("""
            SELECT incident_type, COUNT(*) as count 
            FROM crime_reports 
            GROUP BY incident_type
        """)
        crime_types = cursor.fetchall()
        
        # Status distribution
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM crime_reports 
            GROUP BY status
        """)
        status_dist = cursor.fetchall()
        
        # Monthly trend
        cursor.execute("""
            SELECT 
                DATE_FORMAT(report_date, '%Y-%m') as month,
                COUNT(*) as count
            FROM crime_reports
            GROUP BY month
            ORDER BY month
        """)
        monthly_trend = cursor.fetchall()
        
       # Location data for heatmap
        cursor.execute("""
            SELECT latitude, longitude, incident_type, COUNT(*) as count
            FROM crime_reports
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            GROUP BY latitude, longitude, incident_type
        """)
        heatmap_data = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for item in heatmap_data:
            if 'latitude' in item and item['latitude'] is not None:
                item['latitude'] = float(item['latitude'])
            if 'longitude' in item and item['longitude'] is not None:
                item['longitude'] = float(item['longitude'])
    
    return render_template('admin/admin_analysis.html',
                         crime_types=crime_types,
                         status_dist=status_dist,
                         monthly_trend=monthly_trend,
                         heatmap_data=heatmap_data)

# User logs
@admin_bp.route('/logs')
@admin_login_required
def admin_logs():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get all user logs with user information (if available)
        cursor.execute("""
            SELECT 
                ul.*,
                COALESCE(u.fname, 'Deleted') as fname,
                COALESCE(u.lname, 'User') as lname,
                COALESCE(u.email, 'N/A') as email,
                u.id as user_id
            FROM user_logs ul
            LEFT JOIN users u ON ul.user_id = u.id
            ORDER BY ul.created_at DESC
            LIMIT 100
        """)
        user_logs = cursor.fetchall()

        # Parse user agent information
        for log in user_logs:
            log['parsed_ua'] = parse_user_agent_safe(log.get('user_agent', ''))
            log['device_info'] = f"{log['parsed_ua']['browser']} on {log['parsed_ua']['os']}"

        # Get admin logs
        cursor.execute("""
            SELECT al.*, a.full_name 
            FROM admin_logs al
            JOIN admins a ON al.admin_id = a.id
            ORDER BY al.created_at DESC
            LIMIT 100
        """)
        admin_logs = cursor.fetchall()

        # Get blocked users
        cursor.execute("""
            SELECT bu.user_id, u.fname, u.lname, u.email, a.full_name as blocked_by
            FROM blocked_users bu
            JOIN users u ON bu.user_id = u.id
            JOIN admins a ON bu.admin_id = a.id
        """)
        blocked_users = {user['user_id']: user for user in cursor.fetchall()}

    return render_template('admin/admin_logs.html',
                         user_logs=user_logs,
                         admin_logs=admin_logs,
                         blocked_users=blocked_users)

# Block user
@admin_bp.route('/block_user/<int:user_id>', methods=['POST'])
@admin_login_required
def block_user(user_id):
    reason = request.form['reason']
    
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Check if user is already blocked
        cursor.execute("SELECT * FROM blocked_users WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            flash('User is already blocked', 'warning')
            return redirect(url_for('admin.admin_logs'))
        
        # Block user
        cursor.execute("""
            INSERT INTO blocked_users (user_id, admin_id, reason)
            VALUES (%s, %s, %s)
        """, (user_id, session['admin_id'], reason))
        conn.commit()
        
        log_admin_action("Block User", {
            'user_id': user_id,
            'reason': reason
        })
    
    flash('User blocked successfully', 'success')
    return redirect(url_for('admin.admin_logs'))

# Unblock user
@admin_bp.route('/unblock_user/<int:user_id>')
@admin_login_required
def unblock_user(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blocked_users WHERE user_id = %s", (user_id,))
        conn.commit()
        
        log_admin_action("Unblock User", {
            'user_id': user_id
        })
    
    flash('User unblocked successfully', 'success')
    return redirect(url_for('admin.admin_logs'))

# Admin settings (protected by code)
@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_login_required
@superadmin_required
def admin_settings():
    # Initialize maintenance_mode variable
    maintenance_mode = False
    
    if request.method == 'POST':
        if 'access_code' in request.form:
            code = request.form['access_code']
            if code != '100503':
                flash('Invalid access code', 'danger')
                return redirect(url_for('admin.admin_settings'))
            
            session['settings_access'] = True
            return redirect(url_for('admin.admin_settings'))
        
        # Handle maintenance mode update
        if 'maintenance_mode' in request.form and session.get('settings_access'):
            maintenance_mode = request.form['maintenance_mode'] == '1'
            
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO system_settings (setting_name, setting_value)
                    VALUES ('maintenance_mode', %s)
                    ON DUPLICATE KEY UPDATE setting_value = %s
                """, (str(int(maintenance_mode)), str(int(maintenance_mode))))
                conn.commit()
                
                log_admin_action("Update Maintenance Mode", {
                    'maintenance_mode': maintenance_mode
                })
                
                flash('Maintenance mode updated successfully', 'success')
                session.pop('settings_access', None)
                return redirect(url_for('admin.admin_settings'))
        
        # Create new admin
        if 'create_admin' in request.form and session.get('settings_access'):
            username = request.form['username']
            password = request.form['password']
            full_name = request.form['full_name']
            email = request.form['email']
            is_superadmin = 'is_superadmin' in request.form
            
            with get_db_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                # Check if username exists
                cursor.execute("SELECT id FROM admins WHERE username = %s", (username,))
                if cursor.fetchone():
                    flash('Username already exists', 'danger')
                    return redirect(url_for('admin.admin_settings'))
                
                # Check if email exists
                cursor.execute("SELECT id FROM admins WHERE email = %s", (email,))
                if cursor.fetchone():
                    flash('Email already exists', 'danger')
                    return redirect(url_for('admin.admin_settings'))
                
                # Create admin
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO admins (username, password, full_name, email, is_superadmin)
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, hashed_password, full_name, email, is_superadmin))
                conn.commit()
                
                log_admin_action("Create Admin", {
                    'username': username,
                    'email': email,
                    'is_superadmin': is_superadmin
                })
                
                flash('Admin account created successfully', 'success')
                session.pop('settings_access')
                return redirect(url_for('admin.admin_settings'))
    
    # Get current maintenance mode status
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT setting_value FROM system_settings WHERE setting_name = 'maintenance_mode'")
        result = cursor.fetchone()
        if result:
            maintenance_mode = bool(int(result['setting_value']))

        # Get all admins
        cursor.execute("SELECT * FROM admins ORDER BY created_at DESC")
        admins = cursor.fetchall()
    
    return render_template('admin/admin_settings.html', 
                         admins=admins, 
                         maintenance_mode=maintenance_mode)

@admin_bp.route('/update_maintenance_mode', methods=['POST'])
@admin_login_required
@superadmin_required
def update_maintenance_mode():
    if not session.get('settings_access'):
        flash('Access denied', 'danger')
        return redirect(url_for('admin.admin_settings'))
    
    maintenance_mode = request.form.get('maintenance_mode') == '1'
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO system_settings (setting_name, setting_value)
            VALUES ('maintenance_mode', %s)
            ON DUPLICATE KEY UPDATE setting_value = %s
        """, (str(int(maintenance_mode)), str(int(maintenance_mode))))
        conn.commit()
    
    log_admin_action("Update Maintenance Mode", {
        'maintenance_mode': maintenance_mode
    })
    
    flash('Maintenance mode updated successfully', 'success')
    session.pop('settings_access', None)
    return redirect(url_for('admin.admin_settings'))

# Admin logout
@admin_bp.route('/logout')
def admin_logout():
    if 'admin_id' in session:
        log_admin_action("Admin Logout")
        session.pop('admin_id', None)
        session.pop('admin_name', None)
        session.pop('is_superadmin', None)
    
    flash('You have been logged out', 'info')
    return redirect(url_for('admin.admin_login'))

# Register the blueprint in app.py with:
# from admin import admin_bp
# app.register_blueprint(admin_bp)
