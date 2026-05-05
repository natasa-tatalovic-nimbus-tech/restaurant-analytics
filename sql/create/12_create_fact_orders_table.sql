CREATE TABLE IF NOT EXISTS analytics.fact_orders (
    order_key SERIAL PRIMARY KEY,
    user_key INTEGER REFERENCES analytics.dim_users(user_key), -- who ordered
    restaurant_key INTEGER REFERENCES analytics.dim_restaurants(restaurant_key), -- from where
    time_key INTEGER REFERENCES analytics.dim_time(time_key), -- when oder happpened
    total_price NUMERIC(10, 2), -- 
    item_count INTEGER, -- 
    order_time TIMESTAMP WITH TIME ZONE -- mooment
    -- menu_item is a mistake !
);