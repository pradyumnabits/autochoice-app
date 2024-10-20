curl -X POST http://localhost:8007/customers \
-H "Content-Type: application/json" \
-d '{
  "userId": "12345",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phoneNumber": "123-456-7890",
  "address": "123 Elm Street, Springfield, USA"
}'

curl -X 'GET' \
  'http://localhost:8007/customers/12345' \
  -H 'accept: application/json'


curl -X 'PUT' \
  'http://localhost:8007/customers/12345' \
  -H 'Content-Type: application/json' \
  -d '{
    "userId": "12345",
    "firstName": "John2",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phoneNumber": "987-654-3210",
    "address": "456 Maple Avenue, Springfield, USA"
  }'


curl -X 'DELETE' \
  'http://localhost:8007/customers/12345'

