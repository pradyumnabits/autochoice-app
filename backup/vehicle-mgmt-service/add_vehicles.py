import requests

# Base URL for the FastAPI service
BASE_URL = "http://127.0.0.1:8002/vehicles"

# Vehicle data for various car brands available in India
vehicles_data = [
    {
        "id": "1",
        "make": "Maruti",
        "model": "Swift",
        "year": 2023,
        "price": 700000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "body_type": "Hatchback",
        "image_url": "https://example.com/swift.jpg"
    },
    {
        "id": "2",
        "make": "Tata",
        "model": "Nexon",
        "year": 2023,
        "price": 900000,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "body_type": "SUV",
        "image_url": "https://example.com/nexon.jpg"
    },
    {
        "id": "3",
        "make": "Hyundai",
        "model": "i20",
        "year": 2023,
        "price": 850000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "body_type": "Hatchback",
        "image_url": "https://example.com/i20.jpg"
    },
    {
        "id": "4",
        "make": "Mahindra",
        "model": "Thar",
        "year": 2023,
        "price": 1500000,
        "fuel_type": "Diesel",
        "transmission": "Manual",
        "body_type": "SUV",
        "image_url": "https://example.com/thar.jpg"
    },
    {
        "id": "5",
        "make": "GM",
        "model": "Beat",
        "year": 2019,
        "price": 500000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "body_type": "Hatchback",
        "image_url": "https://example.com/beat.jpg"
    },
    {
        "id": "6",
        "make": "Ford",
        "model": "EcoSport",
        "year": 2022,
        "price": 1100000,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "body_type": "SUV",
        "image_url": "https://example.com/ecosport.jpg"
    },
    {
        "id": "7",
        "make": "Honda",
        "model": "City",
        "year": 2023,
        "price": 1400000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "body_type": "Sedan",
        "image_url": "https://example.com/city.jpg"
    },
    {
        "id": "8",
        "make": "Toyota",
        "model": "Fortuner",
        "year": 2023,
        "price": 3500000,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "body_type": "SUV",
        "image_url": "https://example.com/fortuner.jpg"
    },
    {
        "id": "9",
        "make": "Renault",
        "model": "Kwid",
        "year": 2022,
        "price": 450000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "body_type": "Hatchback",
        "image_url": "https://example.com/kwid.jpg"
    },
    {
        "id": "10",
        "make": "Nissan",
        "model": "Magnite",
        "year": 2023,
        "price": 800000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "body_type": "SUV",
        "image_url": "https://example.com/magnite.jpg"
    },
    {
        "id": "11",
        "make": "Kia",
        "model": "Seltos",
        "year": 2023,
        "price": 1200000,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "body_type": "SUV",
        "image_url": "https://example.com/seltos.jpg"
    },
    {
        "id": "12",
        "make": "Volkswagen",
        "model": "Polo",
        "year": 2022,
        "price": 900000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "body_type": "Hatchback",
        "image_url": "https://example.com/polo.jpg"
    },
    {
        "id": "13",
        "make": "Skoda",
        "model": "Superb",
        "year": 2023,
        "price": 3200000,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "body_type": "Sedan",
        "image_url": "https://example.com/superb.jpg"
    }
]

# Function to add vehicles
def add_vehicle(vehicle):
    response = requests.post(BASE_URL, json=vehicle)
    if response.status_code == 201:
        print(f"Vehicle added successfully: {vehicle['make']} {vehicle['model']}")
    else:
        print(f"Failed to add vehicle: {vehicle['make']} {vehicle['model']}. Status code: {response.status_code}, Error: {response.text}")

# Test adding all vehicles
for vehicle in vehicles_data:
    add_vehicle(vehicle)
