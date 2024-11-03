curl -X POST http://localhost:8000/customers \
    -H "Content-Type: application/json" \
    -d '{
        "userName": "randomID123",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "phoneNumber": "123-456-7890",
        "address": "123 Main St",
        "profileStatus": "Active"
    }'


 curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser123", "password": "testpassword", "firstName": "John", "lastName": "Doe", "email": "johndoe123123@example.com"}'


