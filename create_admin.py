import mysql.connector
from werkzeug.security import generate_password_hash

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='cpaav3'
    )

def create_admin(username, password, full_name, email, is_superadmin=False):
    hashed_password = generate_password_hash(password)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO admins (username, password, full_name, email, is_superadmin)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, hashed_password, full_name, email, is_superadmin))
        conn.commit()
    
    print(f"Admin account created successfully for {username}")

if __name__ == '__main__':
    print("Create a new admin account")
    username = input("Username: ")
    password = input("Password: ")
    full_name = input("Full Name: ")
    email = input("Email: ")
    is_superadmin = input("Is superadmin? (y/n): ").lower() == 'y'
    
    create_admin(username, password, full_name, email, is_superadmin)