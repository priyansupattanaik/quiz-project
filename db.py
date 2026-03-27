import mysql.connector

# -------------------------------------------------------
# db.py — Database connection and auto table creation
# -------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "brucewayne"   # <-- Change if your MySQL password is different
}

DB_NAME = "quiz_system"


def get_connection():
    """Returns a MySQL connection to quiz_system, or None on failure."""
    try:
        con = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
        return con
    except mysql.connector.Error as e:
        print(f"[DB ERROR] Cannot connect to MySQL: {e}")
        return None


def create_tables():
    """
    Creates the database and required tables if they don't exist.
    Also runs a migration to drop the 'email' column if it still exists
    from a previous version of the project.
    """
    try:
        # Connect without a database first so we can create one
        con = mysql.connector.connect(**DB_CONFIG)
        cursor = con.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

        # Table 1: users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INT AUTO_INCREMENT PRIMARY KEY,
                name     VARCHAR(100) NOT NULL,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL
            )
        """)

        # Migration: remove 'email' column if it exists from an older version
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN email")
            con.commit()
        except:
            pass  # Column didn't exist — that's fine, nothing to do

        # Table 2: results — one row per quiz attempt
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id      INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                score   INT NOT NULL,
                total   INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        con.commit()

    except mysql.connector.Error as e:
        print(f"[DB ERROR] Setup failed: {e}")
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass


# Auto-run on import — DB and tables are ready before anything else
try:
    create_tables()
except Exception as e:
    print(f"[DB ERROR] Auto-setup failed: {e}")