from fastapi import FastAPI, HTTPException, Depends
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
    f"sqlite:///{os.path.join(db_directory, 'roadside_assistance.db')}"
)


# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(
            os.path.join(db_directory, "roadside_assistance.db")
        ) as conn:
            cursor = conn.cursor()
            # Create requests table with id as the primary key
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS requests (
                    id TEXT PRIMARY KEY NOT NULL,
                    user_id TEXT NOT NULL,
                    vehicle_id TEXT NOT NULL,
                    location TEXT NOT NULL,
                    status TEXT NOT NULL,
                    provider TEXT
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
class RoadsideAssistanceRequest(BaseModel):
    user_id: str
    vehicle_id: str
    location: str


class RoadsideAssistanceStatus(BaseModel):
    id: str
    user_id: str
    vehicle_id: str
    location: str
    status: str
    provider: str = None


# update data
class UpdateRoadsideAssistanceRequest(BaseModel):
    location: str


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(os.path.join(db_directory, "roadside_assistance.db"))
    return conn


import uuid  # Import uuid for generating unique IDs


def create_request(request: RoadsideAssistanceRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    request_id = str(uuid.uuid4())  # Generate a unique request ID using UUID
    cursor.execute(
        "INSERT INTO requests (id, user_id, vehicle_id, location, status, provider) VALUES (?, ?, ?, ?, ?, ?)",
        (
            request_id,
            request.user_id,
            request.vehicle_id,
            request.location,
            "Pending",
            None,
        ),
    )
    conn.commit()
    conn.close()
    return request_id


def get_all_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()
    conn.close()
    return requests


def get_request_by_id(request_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests WHERE user_id = ?", (request_id,))
    request = cursor.fetchone()
    conn.close()
    return request


def update_request_funn(userid: str, data: UpdateRoadsideAssistanceRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE requests SET location = ? WHERE user_id = ?", (data.location, userid)
    )
    conn.commit()
    conn.close()


# ===========================
# Routing and Business Logic
# ===========================
@app.get("/ping")
def ping():
    return {"msg": "pong-rsa-svc"}

@app.post("/rsa/requests", status_code=201)
def request_roadside_assistance(request: RoadsideAssistanceRequest):
    request_id = create_request(request)
    return {**request.dict(), "id": request_id, "status": "Pending", "provider": None}


# create a methord to update the data
# Step -1 : Get the user_id and updated data from the user via request
# Step -2 : check if the user_id exist or not in db
# Step -3 : if the user is not exist then raise an exception
# Step -4 : if the user is exist then update the data
# step -5 : return the updated data


@app.put("/rsa/requests/{userId}")
def update_request(userId: str, data: UpdateRoadsideAssistanceRequest):
    print(f"Updating request for user {userId} with data: {data}")
    user = get_request_by_id(userId)
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        update_request_funn(userId, data)
        return {"message": "Request updated successfully"}


@app.get("/rsa/requests")
def get_all_roadside_requests():
    requests = get_all_requests()
    return [
        {
            "id": r[0],
            "user_id": r[1],
            "vehicle_id": r[2],
            "location": r[3],
            "status": r[4],
            "provider": r[5],
        }
        for r in requests
    ]


@app.get("/rsa/requests/{requestId}")
def get_roadside_status(requestId: str):
    request = get_request_by_id(requestId)
    print(request)
    print(requestId)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return {
        "id": request[0],
        "user_id": request[1],
        "vehicle_id": request[2],
        "location": request[3],
        "status": request[4],
        "provider": request[5],
    }


# ===========================
# Run the application (Optional - for testing)
# ===========================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8005)
