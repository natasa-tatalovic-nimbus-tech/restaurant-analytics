CREATE TABLE IF NOT EXISTS restaurant.menu_items(
	id SERIAL PRIMARY KEY, 
	restaurant_id INTEGER NOT NULL REFERENCES restaurant.restaurants(id), 
    name VARCHAR(100) NOT NULL,
	description TEXT, 
	price NUMERIC(10,2) NOT NULL CHECK (price > 0)
);
