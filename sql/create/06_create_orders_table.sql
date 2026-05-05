CREATE TABLE IF NOT EXISTS restaurant.orders(
	id SERIAL PRIMARY KEY, 
	user_id INTEGER NOT NULL REFERENCES restaurant.users(id), 
	restaurant_id INTEGER NOT NULL REFERENCES restaurant.restaurants(id), 
	total_price DECIMAL(10,2) CHECK (total_price > 0),
    order_time TIMESTAMP NOT NULL DEFAULT NOW()
    );
