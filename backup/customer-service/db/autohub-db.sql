DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

DROP TABLE IF EXISTS owned_vehicles;

-- Owned Vehicles
CREATE TABLE owned_vehicles (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    purchase_date TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);


INSERT INTO users (username, password_hash)
VALUES
    ('john_doe', 'hashed_password_1'),
    ('jane_smith', 'hashed_password_2');

INSERT INTO customers (user_id, first_name, last_name, email, phone, address)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com', '123-456-7890', '123 Elm St, Springfield, IL, 62704'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com', '987-654-3210', '456 Oak St, Springfield, IL, 62704');



-- Vehicles Table
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    brand VARCHAR(50),
    price DECIMAL(10, 2),
    fuel_type VARCHAR(20),
    engine VARCHAR(50),
    fuel_efficiency VARCHAR(20),
    seating_capacity INT,
    description TEXT
);
-- Indexes to optimize search queries
CREATE INDEX idx_vehicle_brand ON vehicles(brand);
CREATE INDEX idx_vehicle_price ON vehicles(price);

-- Vehicle Images Table
CREATE TABLE vehicle_images (
    id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(id) ON DELETE CASCADE,
    image_url TEXT
);

-- Indexes to optimize search queries
CREATE INDEX idx_vehicle_brand ON vehicles(brand);
CREATE INDEX idx_vehicle_price ON vehicles(price);


-- Test Drive Bookings Table
CREATE TABLE test_drive_bookings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL REFERENCES vehicles(id),
    dealer_id INT,
    booking_date TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('pending', 'confirmed', 'completed', 'canceled'))
);


CREATE TABLE vehicle_purchase_orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT ,
    purchase_date TIMESTAMP,
    total_price DECIMAL(10, 2),
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'canceled'))
);

-- Payment Transactions Table
CREATE TABLE payment_transactions (
    id SERIAL PRIMARY KEY,
    purchase_order_id INT NOT NULL REFERENCES vehicle_purchase_orders(id),
    payment_method VARCHAR(50),
    payment_date TIMESTAMP,
    payment_status VARCHAR(20) CHECK (payment_status IN ('pending', 'completed', 'failed'))
);

-- Maintenance Service Requests Table
CREATE TABLE maintenance_requests (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT ,
    service_date TIMESTAMP,
    service_type VARCHAR(50),
    service_status VARCHAR(20) CHECK (service_status IN ('pending', 'in_progress', 'completed', 'canceled')),
    service_notes TEXT
);

-- Roadside Assistance Requests Table
CREATE TABLE roadside_assistance_requests (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT ,
    request_time TIMESTAMP,
    location TEXT,
    assistance_status VARCHAR(20) CHECK (assistance_status IN ('pending', 'dispatched', 'completed', 'canceled')),
    assistance_notes TEXT
);

--Customer Feedback Table
CREATE TABLE customer_feedback (
    id SERIAL PRIMARY KEY,
    vehicle_id INT NOT NULL,
    username VARCHAR(255) NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on vehicle_id for better performance when querying
CREATE INDEX idx_vehicle_id ON customer_feedback(vehicle_id);


