from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
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
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(db_directory, 'test_drives_bookings.db')}"


# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(os.path.join(db_directory, 'test_drives_bookings.db')) as conn:
            cursor = conn.cursor()
            # Create test_drives table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_drives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            ''')
            # Create bookings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    vehicle_id TEXT NOT NULL,
                    booking_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    transaction_id TEXT NOT NULL  -- New column for transaction ID
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
class TestDrive(BaseModel):
    id: int
    vehicle_id: str
    user_id: str
    date: date
    time: str
    status: str


class TestDriveBooking(BaseModel):
    vehicle_id: str
    user_id: str
    date: date
    time: str


class Booking(BaseModel):
    id: int
    user_id: str
    vehicle_id: str
    booking_date: date
    status: str
    transaction_id: str  # New field for transaction ID


class BookingRequest(BaseModel):
    user_id: str
    vehicle_id: str
    transaction_id: str  # New field for transaction ID


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(os.path.join(db_directory, 'test_drives_bookings.db'))
    return conn


def get_all_test_drives():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_drives")
    test_drives = cursor.fetchall()
    conn.close()
    return test_drives


def get_test_drive_by_id1(test_drive_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_drives WHERE id = ?", (test_drive_id,))
    test_drive = cursor.fetchone()
    conn.close()
    return test_drive


def create_test_drive(test_drive: TestDrive):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO test_drives (vehicle_id, user_id, date, time, status) VALUES (?, ?, ?, ?, ?)",
        (test_drive.vehicle_id, test_drive.user_id, test_drive.date, test_drive.time, test_drive.status)
    )
    conn.commit()
    conn.close()


def get_user_bookings(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings


def get_booking_by_id1(booking_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    booking = cursor.fetchone()
    conn.close()
    return booking


def create_booking(booking: Booking):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (user_id, vehicle_id, booking_date, status, transaction_id) VALUES (?, ?, ?, ?, ?)",
        # Include transaction ID in query
        (booking.user_id, booking.vehicle_id, booking.booking_date, booking.status, booking.transaction_id)
    )
    conn.commit()
    conn.close()


# ===========================
# Test Drives Endpoints
# ===========================
@app.get("/testdrives", response_model=List[TestDrive])
def get_test_drives(vehicle_id: Optional[str] = None, date: Optional[date] = None):
    all_test_drives = get_all_test_drives()
    filtered_test_drives = [
        {
            "id": td[0],
            "vehicle_id": td[1],
            "user_id": td[2],
            "date": td[3],
            "time": td[4],
            "status": td[5]
        } for td in all_test_drives
        if (not vehicle_id or td[1] == vehicle_id) and (not date or td[3] == date.isoformat())
    ]
    return filtered_test_drives


@app.get("/testdrives/{id}", response_model=TestDrive)
def get_test_drive_by_id(id: int):
    test_drive = get_test_drive_by_id1(id)
    if test_drive is None:
        raise HTTPException(status_code=404, detail="Test drive not found")
    return {
        "id": test_drive[0],
        "vehicle_id": test_drive[1],
        "user_id": test_drive[2],
        "date": test_drive[3],
        "time": test_drive[4],
        "status": test_drive[5]
    }


@app.post("/testdrives/book", response_model=TestDrive, status_code=201)
def book_test_drive(booking: TestDriveBooking):
    new_test_drive = TestDrive(
        id=0,  # ID will be auto-incremented
        vehicle_id=booking.vehicle_id,
        user_id=booking.user_id,
        date=booking.date,
        time=booking.time,
        status="Confirmed"
    )
    create_test_drive(new_test_drive)
    return new_test_drive


# ===========================
# Bookings Endpoints
# ===========================
@app.get("/bookings", response_model=List[Booking])
def get_bookings(user_id: str):
    user_bookings = get_user_bookings(user_id)
    return [{
        "id": booking[0],
        "user_id": booking[1],
        "vehicle_id": booking[2],
        "booking_date": booking[3],
        "status": booking[4],
        "transaction_id": booking[5]  # Include transaction ID in response
    } for booking in user_bookings]


@app.get("/bookings/{id}", response_model=Booking)
def get_booking_by_id(id: int):
    booking = get_booking_by_id1(id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {
        "id": booking[0],
        "user_id": booking[1],
        "vehicle_id": booking[2],
        "booking_date": booking[3],
        "status": booking[4],
        "transaction_id": booking[5]  # Include transaction ID in response
    }


@app.post("/bookings", response_model=Booking, status_code=201)
def book_vehicle(booking_request: BookingRequest):
    new_booking = Booking(
        id=0,  # ID will be auto-incremented
        user_id=booking_request.user_id,
        vehicle_id=booking_request.vehicle_id,
        booking_date=date.today(),
        status="Confirmed",
        transaction_id=booking_request.transaction_id  # Include transaction ID from the request
    )
    create_booking(new_booking)
    return new_booking

# ===========================
# Run the application (Optional - for testing)
# ===========================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
