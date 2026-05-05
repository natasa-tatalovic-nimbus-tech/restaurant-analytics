CREATE TABLE IF NOT EXISTS analytics.dim_time (
    time_key    SERIAL PRIMARY KEY,
    full_date   DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL, 
    is_weekend BOOLEAN NOT NULL DEFAULT TRUE
);