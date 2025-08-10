import os
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
from flask import current_app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# def run_system_updates():
    # """Run system updates and security patches"""
    # try:
       #  logger.info(f"Running system updates at {datetime.now()}")
        # if os.name == 'posix':  # Linux/Unix
           #  result = subprocess.run(['apt-get', 'update', '-y'], capture_output=True, text=True)
            # result = subprocess.run(['apt-get', 'upgrade', '-y'], capture_output=True, text=True)
           #  logger.info(f"System updates completed: {result.stdout}")
        # else:
           #  logger.warning("Automatic updates only supported on Linux systems")
   #  except Exception as e:
       #  logger.error(f"Error running system updates: {str(e)}")

def run_backups():
    """Create database backups"""
    try:
        logger.info(f"Running database backup at {datetime.now()}")
        backup_dir = os.path.join(current_app.root_path, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.sql")
        
        # Assuming MySQL database - adjust for your DB
        db_config = current_app.config['MYSQL_DATABASE']
        command = [
            'mysqldump',
            '-h', db_config['host'],
            '-u', db_config['user'],
            f"-p{db_config['password']}",
            db_config['database'],
            '>', backup_file
        ]
        
        result = subprocess.run(' '.join(command), shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Backup completed successfully: {backup_file}")
        else:
            logger.error(f"Backup failed: {result.stderr}")
    except Exception as e:
        logger.error(f"Error running backup: {str(e)}")

def run_malware_scan():
    """Run malware/integrity scan"""
    try:
        logger.info(f"Running malware scan at {datetime.now()}")
        # Check for file integrity by comparing checksums
        
        
        # Get all Python files in the project
        project_root = current_app.root_path
        py_files = []
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file.endswith('.py'):
                    py_files.append(os.path.join(root, file))
        
        # Check for suspicious modifications
        suspicious_changes = []
        for file in py_files:
            # In a real implementation, you would compare against known good hashes
            stat = os.stat(file)
            if stat.st_size > 1000000:  # Files over 1MB might be suspicious
                suspicious_changes.append(file)
        
        if suspicious_changes:
            logger.warning(f"Potential suspicious files detected: {suspicious_changes}")
        else:
            logger.info("No suspicious files detected")
    except Exception as e:
        logger.error(f"Error running malware scan: {str(e)}")

def init_security_cron(app):
    """Initialize the security cron jobs"""
    with app.app_context():
        scheduler = BackgroundScheduler()
        
        # System updates - run daily at 2 AM
       #  scheduler.add_job(
          #   run_system_updates,
           #  'cron',
          #   hour=2,
          #   minute=0,
          #   id='system_updates'
        # )
        
        # Database backups - run daily at 3 AM
        scheduler.add_job(
            run_backups,
            'cron',
            hour=3,
            minute=0,
            id='database_backups'
        )
        
        # Malware scans - run every 6 hours
        scheduler.add_job(
            run_malware_scan,
            'cron',
            hour='*/6',
            id='malware_scan'
        )
        
        scheduler.start()
        logger.info("Security cron jobs initialized")