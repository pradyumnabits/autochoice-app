curl -X 'POST' \
  'http://localhost:8001/auth/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "test_user",
  "password": "test_password",
  "email": "test_user@example.com"
}'


curl -X 'POST' \
  'http://localhost:8001/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "test_user",
  "password": "test_password"
}'

curl -X 'POST' \
  'http://localhost:8001/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "test_user",
    "password": "test_password"
  }'

