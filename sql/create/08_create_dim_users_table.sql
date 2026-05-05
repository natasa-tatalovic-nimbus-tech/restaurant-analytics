CREATE TABLE IF NOT EXISTS analytics.dim_users (
    user_key SERIAL PRIMARY KEY, 
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL, 
    email VARCHAR(100) NOT NULL
);