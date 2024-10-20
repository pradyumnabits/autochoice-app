import requests

BASE_URL = "http://localhost:8001"


# Function to test user registration
def test_register_user():
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": "test_user",
        "password": "test_password",
        "email": "test_user@example.com"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Register Test Passed:", response.json())
    elif response.status_code == 400:
        print("Register Test Failed - Username already exists:", response.json())
    else:
        print("Register Test Failed with unexpected status code:", response.status_code, response.text)


# Function to test token generation
def test_get_token():
    url = f"{BASE_URL}/auth/token"
    payload = {
        "username": "test_user",
        "password": "test_password"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Token Generation Test Passed:", response.json())
    elif response.status_code == 401:
        print("Token Generation Test Failed - Invalid credentials:", response.json())
    else:
        print("Token Generation Test Failed with unexpected status code:", response.status_code, response.text)


# Run the tests
if __name__ == "__main__":
    print("Testing User Registration API:")
    test_register_user()

    print("\nTesting Token Generation API:")
    test_get_token()
