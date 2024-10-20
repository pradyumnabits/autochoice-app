import requests

# Base URL for the FastAPI vehicles endpoint
BASE_URL = "http://127.0.0.1:8002/vehicles"


# Function to get vehicle details by vehicle_id
def get_vehicle_by_id(vehicle_id):
    url = f"{BASE_URL}/{vehicle_id}"
    response = requests.get(url)

    if response.status_code == 200:
        vehicle = response.json()
        print(f"Vehicle Details for ID {vehicle_id}:")
        print(f" - Make: {vehicle['make']}")
        print(f" - Model: {vehicle['model']}")
        print(f" - Year: {vehicle['year']}")
        print(f" - Price: {vehicle['price']}")
        print(f" - ID: {vehicle['vehicle_id']}")
    elif response.status_code == 404:
        print(f"Vehicle with ID {vehicle_id} not found.")
    else:
        print(f"Failed to fetch vehicle details. Status code: {response.status_code}, Error: {response.text}")


# Test cases for retrieving vehicles by vehicle_id
def run_vehicle_id_tests():
    # Test with valid vehicle IDs
    valid_vehicle_ids = ['1', '2', '3']  # Replace with actual vehicle IDs from your database
    for vehicle_id in valid_vehicle_ids:
        get_vehicle_by_id(vehicle_id)

    # Test with an invalid vehicle ID (non-existent ID)
    get_vehicle_by_id("9999")  # An ID that does not exist

    # Test with an invalid format for vehicle ID
    get_vehicle_by_id("invalid_id")  # Invalid ID format


# Run the tests
if __name__ == "__main__":
    run_vehicle_id_tests()
