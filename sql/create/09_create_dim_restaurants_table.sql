-- SCD 2 Type
CREATE TABLE IF NOT EXISTS analytics.dim_restaurants (
    restaurant_key SERIAL PRIMARY KEY, 
    restaurant_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL, 
    adress TEXT, 
    phone VARCHAR(100) NOT NULL, 
    valid_from DATE NOT NULL DEFAULT CURRENT_DATE,
    valid_to DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);