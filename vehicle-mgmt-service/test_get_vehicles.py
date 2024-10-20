import requests

# Base URL for the FastAPI vehicles endpoint
BASE_URL = "http://127.0.0.1:8002/vehicles"


# Function to perform search queries with filters
def get_filtered_vehicles(params):
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        vehicles = response.json()
        if vehicles:
            print(f"Filtered Results for {params}:")
            for vehicle in vehicles:
                print(f" - {vehicle['make']} {vehicle['model']} ({vehicle['year']}) - Price: {vehicle['price']}")
        else:
            print(f"No vehicles found for {params}")
    else:
        print(f"Failed to fetch vehicles with {params}. Status code: {response.status_code}, Error: {response.text}")


# Test cases for different filters
def run_filter_tests():
    # Filter by make
    get_filtered_vehicles({"make": "Maruti"})
    get_filtered_vehicles({"make": "Tata"})

    # Filter by model
    get_filtered_vehicles({"model": "Nexon"})
    get_filtered_vehicles({"model": "i20"})

    # Filter by year
    get_filtered_vehicles({"year": 2023})

    # Filter by make and model
    get_filtered_vehicles({"make": "Hyundai", "model": "i20"})

    # Filter by make and year
    get_filtered_vehicles({"make": "Mahindra", "year": 2023})

    # Filter by non-existent vehicle
    get_filtered_vehicles({"make": "Tesla"})

    # Filter by multiple fields that don't exist together
    get_filtered_vehicles({"make": "Ford", "model": "Mustang", "year": 2025})


# Run the tests
if __name__ == "__main__":
    run_filter_tests()
