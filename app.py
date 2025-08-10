from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from extensions import app, mail, get_db_connection 
from admin import admin_bp
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from cron import init_security_cron
import os
import random
import re
from flask_mail import Mail, Message
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity                                
import numpy as np
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from functools import lru_cache
import threading


app.register_blueprint(admin_bp)

# Global variables for the ML model with thread locks
crime_type_model_lock = threading.Lock()
crime_type_vectorizer = None
crime_type_data = defaultdict(list)

# Cache stopwords
extended_stop_words = None

def load_stopwords():
    global extended_stop_words
    if extended_stop_words is None:
        extended_stop_words = set(stopwords.words('english')).union(
            ['could', 'might', 'must', 'need', 'sha', 'wo', 'would']
        )
    return extended_stop_words

@lru_cache(maxsize=1000)
def custom_tokenizer(text):
    text = text.lower()
    tokens = word_tokenize(text)
    return [token for token in tokens if token.isalpha()]

def train_crime_type_model():
    global crime_type_vectorizer, crime_type_data
    
    with crime_type_model_lock:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT concern, incident_type FROM crime_reports")
            reports = cursor.fetchall()
        
        new_crime_type_data = defaultdict(list)
        for report in reports:
            if report['concern'] and report['incident_type']:
                new_crime_type_data[report['incident_type']].append(report['concern'])
        
        stop_words = load_stopwords()
        
        new_vectorizer = TfidfVectorizer(
            stop_words=list(stop_words),
            tokenizer=custom_tokenizer,
            ngram_range=(1, 2),
            token_pattern=None
        )
        
        all_concerns = []
        for concerns in new_crime_type_data.values():
            all_concerns.extend(concerns)
        
        if all_concerns:
            new_vectorizer.fit(all_concerns)
        
        crime_type_data = new_crime_type_data
        crime_type_vectorizer = new_vectorizer

model_init_thread = threading.Thread(target=train_crime_type_model)
model_init_thread.start()

try:
    if crime_type_vectorizer is not None and not hasattr(crime_type_vectorizer, 'vocabulary_'):
        crime_type_vectorizer.fit([""])
except Exception as e:
    app.logger.error(f"Error training crime type model: {str(e)}")
    crime_type_vectorizer = TfidfVectorizer()
    crime_type_vectorizer.fit([""])

@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@lru_cache(maxsize=128)
def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

def send_otp_email(email, otp):
    msg = Message('Your OTP for Crime Prevention App', recipients=[email])
    msg.body = f'Your OTP is: {otp}'
    mail.send(msg)

@app.before_request
def initialize_otp_attempts():
    if 'otp_attempts' not in session:
        session['otp_attempts'] = 3

@lru_cache(maxsize=1024)
def validate_signup_data(fname, lname, phone, age, email, password):
    errors = []
    
    if not fname or not fname.strip():
        errors.append("First Name is required")
    if not lname or not lname.strip():
        errors.append("Last Name is required")
    if not phone or not re.match(r'^\d{10,15}$', phone):
        errors.append("Enter a valid Phone Number (10-15 digits)")
    if not age or not age.isdigit() or int(age) < 18 or int(age) > 100:
        errors.append("Enter a valid Age (18-100)")
    if not email or not re.match(r'\S+@\S+\.\S+', email):
        errors.append("Enter a valid Email")
    
    if not password or len(password) < 8:
        errors.append("Password must have at least 8 characters")
    elif not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    elif not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    elif not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")
    elif not re.search(r'[^A-Za-z0-9]', password):
        errors.append("Password must contain at least one special character")
    
    return errors

@lru_cache(maxsize=1024)
def validate_login_data(email, password):
    errors = []
    
    if not email or not re.match(r'\S+@\S+\.\S+', email):
        errors.append("Enter a valid Email")
    if not password:
        errors.append("Password is required")
    
    return errors

@lru_cache(maxsize=512)
def parse_user_agent(user_agent_str):
    from user_agents import parse
    ua = parse(user_agent_str)
    return {
        'browser': f"{ua.browser.family} {ua.browser.version_string}",
        'os': f"{ua.os.family} {ua.os.version_string}",
        'device': f"{ua.device.family}"
    }

app.jinja_env.filters['parse_user_agent'] = parse_user_agent

@app.route('/intro')
def intro_animation():
    if 'user_id' in session:
        return redirect(url_for('login'))
    if 'admin_id' in session:
        return redirect(url_for('admin.admin_login'))
    return render_template('intro.html')

@app.route('/')
def home():
    return redirect(url_for('intro_animation'))

@app.route('/login_as')
def login_as():
    if 'user_id' in session:
        return redirect(url_for('login'))
    if 'admin_id' in session:
        return redirect(url_for('admin.admin_login'))
    return render_template('login_as.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        validation_errors = validate_login_data(email, password)
        if validation_errors:
            for error in validation_errors:
                flash(error, 'danger')
            return redirect(url_for('login'))

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT bu.* FROM blocked_users bu
                JOIN users u ON bu.user_id = u.id
                WHERE u.email = %s
            """, (email,))
            if cursor.fetchone():
                flash('Your account has been blocked. Please go to the Baranggay Hall Office.', 'danger')
                return redirect(url_for('login'))
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

        try:
            if user and check_password_hash(user['password'], password):
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    user_agent = request.headers.get('User-Agent')
                    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
                    
                    cursor.execute("""
                        INSERT INTO user_logs (user_id, action, ip_address, user_agent)
                        VALUES (%s, %s, %s, %s)
                    """, (user['id'], 'User Login', ip_address, user_agent))
                    conn.commit()
                    
                session['temp_user_id'] = user['id']
                flash('Please confirm your birthday to complete login.', 'info')
                return redirect(url_for('confirm_birthday'))
            else:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    user_agent = request.headers.get('User-Agent')
                    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
                    
                    cursor.execute("""
                        INSERT INTO user_logs (user_id, action, ip_address, user_agent)
                        VALUES (
                            (SELECT id FROM users WHERE email = %s),
                            'Failed Login Attempt',
                            %s,
                            %s
                        )
                    """, (email, ip_address, user_agent))
                    conn.commit()
                    
                flash('Invalid email or password', 'danger')
        except ValueError as e:
            flash('There was a problem with your account. Please contact support.', 'danger')
            app.logger.error(f"Password hash error for user {email}: {str(e)}")

    return render_template('login.html')

@app.route('/confirm_birthday', methods=['GET', 'POST'])
def confirm_birthday():
    if 'temp_user_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT bu.* FROM blocked_users bu
            WHERE bu.user_id = %s
        """, (session['temp_user_id'],))
        if cursor.fetchone():
            session.pop('temp_user_id', None)
            flash('Your account has been blocked. Please contact support.', 'danger')
            return redirect(url_for('login'))

    if request.method == 'POST':
        month = request.form.get('month')
        day = request.form.get('day')
        year = request.form.get('year')

        if not month or not day or not year:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('confirm_birthday'))

        birthday_str = f"{year}-{month}-{day}"

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date. Please check your input.', 'danger')
            return redirect(url_for('confirm_birthday'))

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT birthday, email FROM users WHERE id = %s", (session['temp_user_id'],))
            user = cursor.fetchone()

        if user and birthday == user['birthday']:
            otp = generate_otp()
            session['otp'] = otp
            session['email'] = user['email']
            print(f"OTP sent to {user['email']}: {otp}")
            send_otp_email(user['email'], otp)
            flash('OTP sent to your email. Please check your inbox.', 'success')
            return redirect(url_for('verify_otp'))
        else:
            flash('Incorrect birthday. Please try again.', 'danger')

    return render_template('confirm_birthday.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'temp_user_id' not in session or 'otp' not in session:
        flash('Please confirm your birthday first.', 'danger')
        return redirect(url_for('confirm_birthday'))

    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT bu.* FROM blocked_users bu
            WHERE bu.user_id = %s
        """, (session['temp_user_id'],))
        if cursor.fetchone():
            session.pop('temp_user_id', None)
            session.pop('otp', None)
            flash('Your account has been blocked. Please contact support.', 'danger')
            return redirect(url_for('login'))

    if request.method == 'POST':
        user_otp = request.form['otp']

        if user_otp == session['otp']:
            session['user_id'] = session.pop('temp_user_id')
            session.pop('otp')
            session.pop('email')
            if 'otp_attempts' in session:
                session.pop('otp_attempts')
            flash('OTP verified. You are now logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html')

@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    if 'temp_user_id' not in session or 'otp_attempts' not in session or session['otp_attempts'] <= 0:
        return jsonify({'success': False, 'message': 'No attempts left.'})

    new_otp = generate_otp()
    session['otp'] = new_otp
    send_otp_email(session['email'], new_otp)
    session['otp_attempts'] -= 1

    return jsonify({'success': True, 'message': 'OTP has been resent.'})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        phone_num = request.form['phone_num']
        age = request.form['age']
        birthday_str = request.form['birthday']
        email = request.form['email']
        password = request.form['password']

        validation_errors = validate_signup_data(fname, lname, phone_num, age, email, password)
        if validation_errors:
            for error in validation_errors:
                flash(error, 'danger')
            return redirect(url_for('signup'))

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('signup'))

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Email already exists. Please log in.', 'danger')
                return redirect(url_for('login'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            cursor.execute("""
                INSERT INTO users (fname, lname, phone_num, age, birthday, email, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, phone_num, age, birthday, email, hashed_password))
            conn.commit()

        flash('Account created successfully! Please log in to continue.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    base_query = "SELECT * FROM crime_reports WHERE user_id = %s"
    params = [user_id]

    if search_query:
        base_query += " AND (complainant_name LIKE %s OR concern LIKE %s OR incident_type LIKE %s OR location LIKE %s)"
        params.extend([f"%{search_query}%"] * 4)

    count_query = f"SELECT COUNT(*) as total FROM ({base_query}) as subquery"
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']

        base_query += " ORDER BY report_date DESC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        cursor.execute(base_query, params)
        reports = cursor.fetchall()
    
    return render_template('dashboard.html', 
                         reports=reports, 
                         search_query=search_query,
                         page=page,
                         per_page=per_page,
                         total=total)

@app.route('/user_analytics')
def user_analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as total FROM crime_reports WHERE user_id = %s", (user_id,))
        total_reports = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as pending FROM crime_reports WHERE user_id = %s AND status = 'Pending'", (user_id,))
        pending_reports = cursor.fetchone()['pending']

        cursor.execute("SELECT COUNT(*) as resolved FROM crime_reports WHERE user_id = %s AND status = 'Resolved'", (user_id,))
        resolved_reports = cursor.fetchone()['resolved']

        cursor.execute("""
            SELECT
                COALESCE(incident_type, 'Unknown') as incident_type,
                COUNT(*) as count
            FROM crime_reports
            WHERE user_id = %s
            GROUP BY incident_type
            ORDER BY count DESC
        """, (user_id,))
        type_data = cursor.fetchall()

        cursor.execute("""
            SELECT
                COALESCE(location, 'Unknown') as location,
                COUNT(*) as count
            FROM crime_reports
            WHERE user_id = %s
            GROUP BY location
            ORDER BY count DESC
            LIMIT 5
        """, (user_id,))
        location_data = cursor.fetchall()

        cursor.execute("""
            SELECT
                COALESCE(status, 'Pending') as status,
                COUNT(*) as count
            FROM crime_reports
            WHERE user_id = %s
            GROUP BY status
            ORDER BY
                CASE status
                    WHEN 'Pending' THEN 1
                    WHEN 'Received' THEN 2
                    WHEN 'In Progress' THEN 3
                    WHEN 'Resolved' THEN 4
                    ELSE 5
                END
        """, (user_id,))
        status_data = cursor.fetchall()

        cursor.execute("""
            SELECT
                latitude,
                longitude,
                COALESCE(incident_type, 'Other') as incident_type,
                COALESCE(location, 'Unknown') as location,
                DATE_FORMAT(report_date, '%%Y-%%m-%%d') as report_date,
                status
            FROM crime_reports
            WHERE user_id = %s
            AND latitude IS NOT NULL
            AND longitude IS NOT NULL
            AND latitude BETWEEN 10.5 AND 11.0
            AND longitude BETWEEN 122.4 AND 122.7
        """, (user_id,))
        map_data = cursor.fetchall()

    serializable_map_data = []
    for item in map_data:
        try:
            serializable_map_data.append({
                'latitude': float(item['latitude']) if item['latitude'] is not None else None,
                'longitude': float(item['longitude']) if item['longitude'] is not None else None,
                'incident_type': item['incident_type'],
                'location': item['location'],
                'report_date': item['report_date'],
                'status': item['status']
            })
        except (ValueError, TypeError) as e:
            app.logger.error(f"Error processing map data: {e}")
            continue

    return render_template('user_analytics.html',
                           total_reports=total_reports,
                           pending_reports=pending_reports,
                           resolved_reports=resolved_reports,
                           type_data=type_data,
                           location_data=location_data,
                           status_data=status_data,
                           map_data=serializable_map_data)
@app.route('/report', methods=['GET', 'POST'])
def report_crime():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        complainant_name = request.form['complainant_name']
        concern = request.form['concern']
        incident_type = request.form['incident_type']  # This will now accept any text
        location = request.form['location']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        report_date = datetime.now().strftime('%Y-%m-%d')
        user_id = session['user_id']

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT fname, lname FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
        
        registered_name = f"{user['fname']} {user['lname']}"
        if complainant_name.lower() != registered_name.lower():
            return jsonify({'category': 'danger', 'message': 'Name must match your registered account name'})

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                INSERT INTO crime_reports 
                (complainant_name, concern, incident_type, location, latitude, longitude, report_date, user_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
            """, (complainant_name, concern, incident_type, location, latitude, longitude, report_date, user_id))
            conn.commit()
            
            threading.Thread(target=train_crime_type_model).start()
            
            return jsonify({'category': 'success', 'message': 'Concern submitted successfully!'})

    return render_template('report_crime.html')



@app.route('/delete_report/<int:report_id>', methods=['GET'])
def delete_report(report_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM crime_reports WHERE id = %s AND user_id = %s", (report_id, user_id))
        conn.commit()

    flash('Report deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                otp = generate_otp()
                session['reset_otp'] = otp
                session['reset_email'] = email
                send_otp_email(email, otp)
                flash('OTP sent to your email. Please check your inbox.', 'success')
                return redirect(url_for('verify_reset_otp'))
            else:
                flash('Email not found. Please try again.', 'danger')

    return render_template('forgot_password.html')

@app.route('/verify_reset_otp', methods=['GET', 'POST'])
def verify_reset_otp():
    if 'reset_otp' not in session or 'reset_email' not in session:
        flash('Please request an OTP first.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        user_otp = request.form['otp']

        if user_otp == session['reset_otp']:
            session['allow_reset'] = True
            flash('OTP verified. You can now reset your password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'allow_reset' not in session or not session['allow_reset']:
        flash('Please verify your OTP first.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('reset_password'))

        hashed_password = generate_password_hash(new_password)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
            conn.commit()

        session.pop('reset_otp')
        session.pop('reset_email')
        session.pop('allow_reset')

        flash('Your password has been reset successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    email = session.get('reset_email', '')
    return render_template('reset_password.html', email=email)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('temp_user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/validate_name')
def validate_name():
    if 'user_id' not in session:
        return jsonify({'valid': False})
    
    full_name = request.args.get('full_name', '').strip()
    if not full_name:
        return jsonify({'valid': False})
    
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT fname, lname FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
    
    if user:
        registered_name = f"{user['fname']} {user['lname']}".lower()
        return jsonify({'valid': full_name.lower() == registered_name})
    
    return jsonify({'valid': False})

def check_maintenance_mode():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            # First check if the table exists
            cursor.execute("""
                SELECT COUNT(*) as table_exists 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = 'system_settings'
            """)
            table_exists = cursor.fetchone()['table_exists']
            
            if not table_exists:
                return False
                
            cursor.execute("SELECT setting_value FROM system_settings WHERE setting_name = 'maintenance_mode'")
            result = cursor.fetchone()
            if result and bool(int(result['setting_value'])):
                return True
    except Exception as e:
        app.logger.error(f"Error checking maintenance mode: {str(e)}")
    return False

@app.before_request
def check_for_maintenance():
    # Skip maintenance check for these paths
    if request.path.startswith('/admin') or request.path.startswith('/static'):
        return
    
    if request.path == '/maintenance':
        return
    
    if check_maintenance_mode():
        return render_template('maintenance.html', current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 503

@app.route('/maintenance')
def maintenance_page():
    return render_template('maintenance.html', current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 503

init_security_cron(app)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)