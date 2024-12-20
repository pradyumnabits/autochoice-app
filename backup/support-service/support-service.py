from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sqlite3
from sqlite3 import Error

# FastAPI app initialization
app = FastAPI()

# ===========================
# Database Setup
# ===========================
# Create a directory for the database if it doesn't exist
db_directory = os.path.join(
    os.getcwd(), "data"
)  # 'data' folder in the current directory
os.makedirs(db_directory, exist_ok=True)  # Create the directory if it doesn't exist
SQLALCHEMY_DATABASE_URL = (
    f"sqlite:///{os.path.join(db_directory, 'service_support.db')}"
)


# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(os.path.join(db_directory, "service_support.db")) as conn:
            cursor = conn.cursor()
            # Create service appointments table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS service_appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    vehicle_id TEXT NOT NULL,
                    appointment_date TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    status TEXT DEFAULT 'Scheduled'
                )
            """
            )
            # Create service history table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS service_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    vehicle_id TEXT NOT NULL,
                    service_date TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    description TEXT
                )
            """
            )
            conn.commit()
            print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")


# Call the function to initialize the database
initialize_database()


# ===========================
# Pydantic Schemas
# ===========================
class ServiceAppointment(BaseModel):
    user_id: str
    vehicle_id: str
    appointment_date: str
    service_type: str


class ServiceHistory(BaseModel):
    user_id: str
    vehicle_id: str
    service_date: str
    service_type: str
    description: str


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(os.path.join(db_directory, "service_support.db"))
    return conn


def create_service_appointment(appointment: ServiceAppointment):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO service_appointments (user_id, vehicle_id, appointment_date, service_type) VALUES (?, ?, ?, ?)",
        (
            appointment.user_id,
            appointment.vehicle_id,
            appointment.appointment_date,
            appointment.service_type,
        ),
    )
    conn.commit()
    conn.close()


def get_service_history(user_id: str, vehicle_id: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if vehicle_id:
        print("vehicle_id:", vehicle_id)
        cursor.execute(
            "SELECT * FROM service_appointments WHERE user_id = ? AND vehicle_id = ?",
            (user_id, vehicle_id),
        )
    else:
        print("user_id:", user_id)
        cursor.execute(
            "SELECT * FROM service_appointments WHERE user_id = ?", (user_id,)
        )
    history = cursor.fetchall()
    conn.close()
    return history


def get_all_service_appointments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM service_appointments")
    appointments = cursor.fetchall()
    conn.close()
    return appointments


# ===========================
# Routing and Business Logic
# ===========================
@app.post("/service/schedule", status_code=201)
def schedule_service(appointment: ServiceAppointment):
    create_service_appointment(appointment)
    return appointment


@app.get("/service/history")
def list_service_history(user_id: str, vehicle_id: str = None):
    history = get_service_history(user_id, vehicle_id)
    if not history:
        raise HTTPException(status_code=404, detail="No service history found")
    return [
        {
            "user_id": h[1],
            "vehicle_id": h[2],
            "service_date": h[3],
            "service_type": h[4],
            "description": h[5],
        }
        for h in history
    ]


@app.get("/service/appointments")
def list_service_appointments():
    appointments = get_all_service_appointments()
    return [
        {
            "id": a[0],
            "user_id": a[1],
            "vehicle_id": a[2],
            "appointment_date": a[3],
            "service_type": a[4],
            "status": a[5],
        }
        for a in appointments
    ]


# ===========================
# Run the application (Optional - for testing)
# ===========================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8004)
