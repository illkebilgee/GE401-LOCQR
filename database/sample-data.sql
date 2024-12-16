-- 1. Insert sample gyms
INSERT INTO gyms (id, name, address, contact_info, created_at) VALUES
    (1, 'Downtown Fitness', '123 Main St, Downtown', '555-1234', '2024-01-10 08:00:00+00'),
    (2, 'Uptown Gym', '456 Elm St, Uptown', '555-5678', '2024-02-15 09:30:00+00');

-- 2. Insert sample users
INSERT INTO users (id, username, password_hash, role, gym_id, created_at) VALUES
    (1, 'admin_downtown', 'hashed_password_1', 'admin', 1, '2024-01-11 10:00:00+00'),
    (2, 'staff_downtown', 'hashed_password_2', 'staff', 1, '2024-01-12 11:15:00+00'),
    (3, 'member_uptown_john', 'hashed_password_3', 'member', 2, '2024-02-16 12:20:00+00'),
    (4, 'member_downtown_jane', 'hashed_password_4', 'member', 1, '2024-03-01 14:45:00+00');

-- 3. Insert sample lockers
INSERT INTO lockers (id, locker_number, qr_code_data, is_occupied, occupied_by, gym_id, created_at) VALUES
    -- Lockers for Downtown Fitness (gym_id = 1)
    (1, 'D101', 'QRDATA_D101', FALSE, NULL, 1, '2024-01-10 08:05:00+00'),
    (2, 'D102', 'QRDATA_D102', TRUE, 4, 1, '2024-01-10 08:10:00+00'),
    (3, 'D103', 'QRDATA_D103', FALSE, NULL, 1, '2024-01-10 08:15:00+00'),
    
    -- Lockers for Uptown Gym (gym_id = 2)
    (4, 'U201', 'QRDATA_U201', TRUE, 3, 2, '2024-02-15 09:35:00+00'),
    (5, 'U202', 'QRDATA_U202', FALSE, NULL, 2, '2024-02-15 09:40:00+00'),
    (6, 'U203', 'QRDATA_U203', FALSE, NULL, 2, '2024-02-15 09:45:00+00');

-- 4. Insert sample access logs
INSERT INTO access_logs (id, user_id, locker_id, action, timestamp) VALUES
    -- Logs for Downtown Fitness
    (1, 1, 2, 'lock', '2024-03-01 15:00:00+00'),      -- Admin locks Jane's locker
    (2, 4, 2, 'unlock', '2024-03-01 15:05:00+00'),    -- Jane unlocks her locker
    (3, 2, 1, 'access_denied', '2024-03-02 09:00:00+00'), -- Staff denied access to Locker 1
    (4, 4, 3, 'lock', '2024-03-02 09:10:00+00'),      -- Jane locks Locker 3
    
    -- Logs for Uptown Gym
    (5, 1, 4, 'access_denied', '2024-04-01 10:00:00+00'), -- Admin denied access to John's locker
    (6, 3, 4, 'unlock', '2024-04-01 10:15:00+00'),    -- John unlocks his locker
    (7, 3, 5, 'lock', '2024-04-02 11:00:00+00'),      -- John locks Locker 5
    (8, 2, 6, 'access_denied', '2024-04-03 12:00:00+00'); -- Staff denied access to Locker 6