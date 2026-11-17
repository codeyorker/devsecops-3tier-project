CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending'
        CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
