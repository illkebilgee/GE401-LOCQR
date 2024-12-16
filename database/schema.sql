
-- Create ENUM type for user roles
CREATE TYPE user_role AS ENUM ('admin', 'member', 'staff');

-- Create ENUM type for access log actions
CREATE TYPE access_action AS ENUM ('lock', 'unlock', 'access_denied');

-- Create the Gyms table
CREATE TABLE gyms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'member',
    gym_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE SET NULL
);

-- Create the Lockers table
CREATE TABLE lockers (
    id SERIAL PRIMARY KEY,
    locker_number VARCHAR(50) NOT NULL,
    qr_code_data VARCHAR(255) NOT NULL,
    is_occupied BOOLEAN DEFAULT FALSE,
    occupied_by INTEGER,
    gym_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (occupied_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE,
    UNIQUE (locker_number, gym_id)
);

-- Create the Access_Logs table
CREATE TABLE access_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    locker_id INTEGER NOT NULL,
    action access_action NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (locker_id) REFERENCES lockers(id) ON DELETE CASCADE
);

-- Optional: Create indexes to improve query performance
CREATE INDEX idx_users_gym_id ON users(gym_id);
CREATE INDEX idx_lockers_gym_id ON lockers(gym_id);
CREATE INDEX idx_lockers_occupied_by ON lockers(occupied_by);
CREATE INDEX idx_access_logs_user_id ON access_logs(user_id);
CREATE INDEX idx_access_logs_locker_id ON access_logs(locker_id);