--Schema Setup for Safe-Travels Navigator
DROP TABLE IF EXISTS route_history;
DROP TABLE IF EXISTS saved_locations;
DROP TABLE IF EXISTS users;

--Table Users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Table 'saved_locations'
CREATE TABLE saved_locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    alias VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

--Table 'route_history'
CREATE TABLE route_history (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    start_location_id INT,
    end_location VARCHAR(255) NOT NULL,
    hazards_avoided INT DEFAULT 0,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (start_location_id) REFERENCES saved_locations(location_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

--Sample Data for testing
INSERT INTO users (username, emergency_contact_phone) 
VALUES 
    ('night_owl_99', '+15550198372'),
    ('study_grinder', '+15550123948');

INSERT INTO saved_locations (user_id, alias, address) 
VALUES 
    (1, 'Home', '123 NW 14th St, Corvallis, OR'),
    (1, 'Library', 'Valley Library, Corvallis, OR');

INSERT INTO route_history (user_id, start_location_id, end_location, hazards_avoided) 
VALUES 
    (1, 2, 'Dixon Recreation Center', 2);
