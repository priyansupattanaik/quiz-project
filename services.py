from db import get_connection
from validators import validate_username, validate_password
from models import QuizUser

# -------------------------------------------------------
# services.py — All database service functions (CRUD)
# Requirement: Full CRUD operations on MySQL
# -------------------------------------------------------

# ---- CREATE: Register a new user ----
def register():
    try:
        print("\n--- New Account Registration ---")
        name     = input("Enter your Full Name : ").strip()
        username = input("Enter Username (3-20 chars, letters/digits only): ").strip()
        password = input("Enter Password (min 4 characters): ").strip()

        # Regex validation
        if not validate_username(username):
            print("[X] Invalid Username. Use 3-20 letters or digits only.")
            return
        if not validate_password(password):
            print("[X] Password must be at least 4 characters.")
            return

        con = get_connection()
        if con is None:
            return

        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
            (name, username, password)
        )
        con.commit()
        print("\n[OK] Account Registered Successfully!")

    except Exception as e:
        print(f"[ERROR] Registration failed: {e}")
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass


# ---- READ: Login ----
def login():
    try:
        print("\n--- Login ---")
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        con = get_connection()
        if con is None:
            return None

        cursor = con.cursor()
        cursor.execute(
            "SELECT id, name, username FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        row = cursor.fetchone()

        if row:
            user_id, name, db_username = row
            # OOP: instantiate QuizUser (Inheritance + Encapsulation)
            logged_in_user = QuizUser(user_id, name, db_username)
            logged_in_user.set_password(password)
            print(f"\n[OK] Login Successful! Welcome, {name}!")
            return logged_in_user
        else:
            print("\n[X] Incorrect username or password. Try again.")
            return None

    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return None
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass


# ---- READ: Fetch results for analytics ----
def get_user_data(user_id):
    try:
        con = get_connection()
        if con is None:
            return None

        cursor = con.cursor()
        cursor.execute(
            "SELECT u.name, r.score, r.total FROM results r JOIN users u ON r.user_id = u.id WHERE u.id = %s",
            (user_id,)
        )
        return cursor.fetchall()

    except Exception as e:
        print(f"[ERROR] Could not fetch data: {e}")
        return None
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass


# ---- UPDATE: Change password ----
def update_password(user_obj):
    try:
        new_password = input("Enter new password (min 4 characters): ").strip()

        if not validate_password(new_password):
            print("[X] Password must be at least 4 characters.")
            return

        con = get_connection()
        if con is None:
            return

        cursor = con.cursor()
        cursor.execute(
            "UPDATE users SET password = %s WHERE id = %s",
            (new_password, user_obj.user_id)
        )
        con.commit()
        user_obj.set_password(new_password)   # Encapsulation: update in-memory object
        print("[OK] Password Updated Successfully!")

    except Exception as e:
        print(f"[ERROR] Password update failed: {e}")
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass


# ---- DELETE: Remove account ----
def delete_account(user_id):
    try:
        confirm = input("Are you sure you want to DELETE your account? (yes/no): ").strip()

        if confirm.lower() == "yes":
            con = get_connection()
            if con is None:
                return False

            cursor = con.cursor()
            # Results cascade-delete via FK; we also delete explicitly for clarity
            cursor.execute("DELETE FROM results WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            con.commit()
            print("[OK] Your account and all data have been permanently deleted.")
            return True
        else:
            print("[--] Account deletion cancelled.")
            return False

    except Exception as e:
        print(f"[ERROR] Account deletion failed: {e}")
        return False
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass


# ---- CREATE: Save quiz result ----
def save_result(user_id, score, total):
    try:
        con = get_connection()
        if con is None:
            return

        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO results (user_id, score, total) VALUES (%s, %s, %s)",
            (user_id, score, total)
        )
        con.commit()
        print("[OK] Result saved to database.")

    except Exception as e:
        print(f"[ERROR] Could not save result: {e}")
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass
