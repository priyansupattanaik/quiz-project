import mysql.connector

# database setup and connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="brucewayne",
        database="quiz_system"
    )

def setup_db():
    conn = mysql.connector.connect(host="localhost", user="root", password="brucewayne")
    cursor = conn.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS quiz_system")
    cursor.execute("USE quiz_system")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        username VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        score INT,
        total INT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# run this automatically when imported
setup_db()