from db import get_connection
from validators import validate_username, validate_password
from models import QuizUser

# user crud functions
def register():
    name = input("Enter full name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if not validate_username(username):
        print("Invalid username. Use 3-20 letters/digits.")
        return
    if not validate_password(password):
        print("Password must be at least 4 characters.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
            (name, username, password)
        )
        conn.commit()
        print("Registered successfully!")
    except:
        print("Error: Username might already exist.")
    
    cursor.close()
    conn.close()


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, username FROM users WHERE username=%s AND password=%s", (username, password))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if row:
        print("Login successful!")
        user = QuizUser(row[0], row[1], row[2])
        user.set_password(password)
        return user
    else:
        print("Invalid credentials.")
        return None


def update_password(user):
    new_pwd = input("Enter new password: ")
    if not validate_password(new_pwd):
        print("Password too short.")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_pwd, user.uid))
    conn.commit()
    user.set_password(new_pwd)
    print("Password updated!")
    
    cursor.close()
    conn.close()


def delete_account(user):
    ans = input("Delete account permanently? (yes/no): ")
    if ans == "yes":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user.uid,))
        conn.commit()
        print("Account deleted.")
        cursor.close()
        conn.close()
        return True
    return False


def save_result(uid, score, total):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (user_id, score, total) VALUES (%s, %s, %s)", (uid, score, total))
    conn.commit()
    cursor.close()
    conn.close()