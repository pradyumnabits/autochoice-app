import requests
import uuid

BASE_URL = "http://localhost:8007/customers"

# Function to generate a random alphanumeric userId
def generate_random_user_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric userId

# Test Data
customer_data = {
    "userId": generate_random_user_id(),  # Random alphanumeric customerId
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phoneNumber": "123-456-7890",
    "address": "123 Elm Street, Springfield, USA"
}

updated_customer_data = {
    "firstName": "John",
    "lastName": "Smith",
    "email": "john.smith@example.com",
    "phoneNumber": "987-654-3210",
    "address": "456 Oak Avenue, Springfield, USA"
}

def test_create_customer():
    print("\n--- Testing Create Customer API ---")
    response = requests.post(BASE_URL, json=customer_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return customer_data['userId']  # Return the generated userId for further testing

def test_get_customers():
    print("\n--- Testing Get All Customers API ---")
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_customer_by_id(user_id):
    print(f"\n--- Testing Get Customer by ID API for userId: {user_id} ---")
    response = requests.get(f"{BASE_URL}/{user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Customer not found")

def test_update_customer(user_id):
    print(f"\n--- Testing Update Customer API for userId: {user_id} ---")
    response = requests.put(f"{BASE_URL}/{user_id}", json=updated_customer_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Customer update failed")

def test_delete_customer(user_id):
    print(f"\n--- Testing Delete Customer API for userId: {user_id} ---")
    response = requests.delete(f"{BASE_URL}/{user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Customer deleted successfully")
    else:
        print("Customer deletion failed")

if __name__ == "__main__":
    # Run the tests
    user_id = test_create_customer()  # Generate a random userId during customer creation
    test_get_customers()
    test_get_customer_by_id(user_id)
    test_update_customer(user_id)
    test_get_customer_by_id(user_id)  # Check updated customer details
    test_delete_customer(user_id)
    test_get_customers()  # Check remaining customers
