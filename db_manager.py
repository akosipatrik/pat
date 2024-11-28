import sqlite3
import bcrypt

# Function to create the database and users table if it doesn't exist
def setup_database():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error setting up database: {e}")

# Function to register a new user (hashes the password before saving)
def register_user(username, password):
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user into the database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists!")

# Function to check if a username and password are valid during login
def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    return False
