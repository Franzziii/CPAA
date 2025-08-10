from flask import Flask, current_app
from flask_mail import Mail
import mysql.connector
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = '100503'

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'crimepreventionappandanalysis@gmail.com'
app.config['MAIL_PASSWORD'] = 'wzidzsjczlmveork'  
app.config['MAIL_DEFAULT_SENDER'] = 'crimepreventionappandanalysis@gmail.com'

mail = Mail(app)

# Database connection with context manager support
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='cpaav5'
        )
        yield conn
    except Exception as e:
        current_app.logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

@contextmanager
def get_db_cursor():
    with get_db_connection() as conn:
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Database operation error: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()