from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sqlite3
from sqlite3 import Error

app = FastAPI()

# ===========================
# Database Setup
# ===========================
db_directory = os.path.join(os.getcwd(), 'data')
os.makedirs(db_directory, exist_ok=True)
db_file = os.path.join(db_directory, 'customers6.db')

# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    userId TEXT PRIMARY KEY NOT NULL,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phoneNumber TEXT,
                    address TEXT,
                    profileStatus TEXT DEFAULT 'active'  -- Add default status 'active'
                )
            ''')
            conn.commit()
            print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")

initialize_database()

# ===========================
# Pydantic Schemas
# ===========================
class Customer(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: str = None
    address: str = None
    profileStatus: str = "ACTIVE"  # New field with a default value

# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(db_file)
    return conn

def get_all_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

def get_customer_by_id(userId: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE userId = ?", (userId,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (userId, firstName, lastName, email, phoneNumber, address, profileStatus) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (customer.userId, customer.firstName, customer.lastName, customer.email, customer.phoneNumber, customer.address, customer.profileStatus)
    )
    conn.commit()
    conn.close()

def update_customer(userId: str, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET firstName = ?, lastName = ?, email = ?, phoneNumber = ?, address = ?, profileStatus = ? WHERE userId = ?",
        (customer.firstName, customer.lastName, customer.email, customer.phoneNumber, customer.address, customer.profileStatus, userId)
    )
    conn.commit()
    conn.close()

def delete_customer(userId: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET profileStatus = 'inactive' WHERE userId = ?", (userId,))
    conn.commit()
    conn.close()

# ===========================
# Routing and Business Logic
# ===========================
@app.get("/customers")
def list_customers():
    customers = get_all_customers()
    return [{"userId": c[0], "firstName": c[1], "lastName": c[2], "email": c[3], "phoneNumber": c[4], "address": c[5], "profileStatus": c[6]} for c in customers]

@app.post("/customers", status_code=201)
def create_new_customer(customer: Customer):
    create_customer(customer)
    return customer

@app.get("/customers/{userId}")
def get_customer(userId: str):
    customer = get_customer_by_id(userId)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"userId": customer[0], "firstName": customer[1], "lastName": customer[2], "email": customer[3], "phoneNumber": customer[4], "address": customer[5], "profileStatus": customer[6]}

@app.put("/customers/{userId}")
def update_existing_customer(userId: str, customer: Customer):
    existing_customer = get_customer_by_id(userId)
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_customer(userId, customer)
    return customer

@app.delete("/customers/{userId}", status_code=204)
def remove_customer(userId: str):
    existing_customer = get_customer_by_id(userId)
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(userId)
