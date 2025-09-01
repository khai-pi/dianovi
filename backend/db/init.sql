CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INT,
    diagnosis TEXT
);

INSERT INTO users (username, email, password_hash) VALUES 
    ('admin', 'admin@example.com', '$2b$12$hashed_password_here'),
    ('testuser', 'test@example.com', '$2b$12$another_hashed_password')
ON CONFLICT (username) DO NOTHING;