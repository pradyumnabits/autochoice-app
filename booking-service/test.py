import httpx
import asyncio
from datetime import date

# FastAPI application URL
BASE_URL = "http://127.0.0.1:8003"

# Sample data for testing
user_id = "user123"
vehicle_id = "vehicle456"
test_drive_id = 1  # Adjust this ID based on your test data
test_drive_date = date.today()
test_drive_time = "10:00 AM"

async def create_test_drive():
    # Create a test drive
    test_drive_data = {
        "vehicle_id": vehicle_id,
        "user_id": user_id,
        "date": test_drive_date.isoformat(),
        "time": test_drive_time,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/testdrives/book", json=test_drive_data)
        if response.status_code == 201:
            print("Test drive created successfully:", response.json())
        else:
            print("Failed to create test drive:", response.status_code, response.text)

async def get_all_test_drives():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/testdrives")
        if response.status_code == 200:
            test_drives = response.json()
            print("All test drives retrieved successfully:", test_drives)
        else:
            print("Failed to retrieve test drives:", response.status_code, response.text)

async def get_test_drive_by_id():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/testdrives/{test_drive_id}")
        if response.status_code == 200:
            test_drive = response.json()
            print("Test drive retrieved successfully:", test_drive)
        else:
            print("Failed to retrieve test drive:", response.status_code, response.text)

async def book_test_drive():
    # Book a test drive (assuming the test drive already exists)
    booking_data = {
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "date": test_drive_date.isoformat(),
        "time": test_drive_time,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/testdrives/book", json=booking_data)
        if response.status_code == 201:
            print("Test drive booked successfully:", response.json())
        else:
            print("Failed to book test drive:", response.status_code, response.text)

async def get_user_bookings():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/bookings?user_id={user_id}")
        if response.status_code == 200:
            bookings = response.json()
            print("User bookings retrieved successfully:", bookings)
        else:
            print("Failed to retrieve bookings:", response.status_code, response.text)

async def get_booking_by_id():
    booking_id = 1  # Adjust this ID based on your test data
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/bookings/{booking_id}")
        if response.status_code == 200:
            booking = response.json()
            print("Booking retrieved successfully:", booking)
        else:
            print("Failed to retrieve booking:", response.status_code, response.text)

async def main():
    await create_test_drive()
    await get_all_test_drives()
    await get_test_drive_by_id()
    await book_test_drive()
    await get_user_bookings()
    await get_booking_by_id()

# Run the test
if __name__ == "__main__":
    asyncio.run(main())
