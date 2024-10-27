import os

# Set the database directory
db_directory = os.path.join(os.getcwd(), 'data')  # 'data' folder in the current directory
os.makedirs(db_directory, exist_ok=True)  # Create the directory if it doesn't exist

import sqlite3
print(sqlite3.sqlite_version)


print("Current Working Directory:", os.getcwd())

