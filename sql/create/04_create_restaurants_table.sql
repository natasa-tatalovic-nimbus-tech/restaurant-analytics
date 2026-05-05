CREATE TABLE IF NOT EXISTS restaurant.restaurants(
	id SERIAL PRIMARY KEY, 
	name VARCHAR(100) NOT NULL, 
	address TEXT, 
	phone VARCHAR(50)
);