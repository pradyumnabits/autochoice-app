from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import os
import sqlite3
from sqlite3 import Error

# FastAPI app initialization
app = FastAPI()

# ===========================
# Database Setup
# ===========================
# Create a directory for the database if it doesn't exist
db_directory = os.path.join(os.getcwd(), 'data')  # 'data' folder in the current directory
os.makedirs(db_directory, exist_ok=True)  # Create the directory if it doesn't exist
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(db_directory, 'test.db')}"


# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(os.path.join(db_directory, 'test.db')) as conn:
            cursor = conn.cursor()
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")


# Call the function to initialize the database
initialize_database()


# ===========================
# Pydantic Schemas
# ===========================
class User(BaseModel):
    username: str
    email: str
    password: str


class AuthUser(BaseModel):
    username: str
    password: str


# ===========================
# Business Logic (Password hashing)
# ===========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(os.path.join(db_directory, 'test.db'))
    return conn


def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    db_user = cursor.fetchone()

    if db_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password and insert the new user
    hashed_password = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
        (user.username, user.email, hashed_password)
    )
    conn.commit()
    conn.close()

    return {"username": user.username, "email": user.email}


def get_user_by_username(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


# ===========================
# Routing and Business Logic
# ===========================
@app.post("/auth/register")
def register_user(user: User):
    user_data = create_user(user)
    return {"msg": "User registered successfully", "user": user_data}


@app.post("/auth/login")
def login_user(user: AuthUser):
    db_user = get_user_by_username(user.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Verify password
    if not verify_password(user.password, db_user[3]):  # Assuming hashed_password is at index 3
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"msg": "Login successful", "user": {"username": db_user[1], "email": db_user[
        2]}}  # Assuming username is at index 1 and email at index 2

# ===========================
# Run the application (Optional - for testing)
# ===========================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8001)
