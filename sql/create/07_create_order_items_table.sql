CREATE TABLE IF NOT EXISTS restaurant.order_items(
	id SERIAL PRIMARY KEY, 
    order_id INTEGER NOT NULL REFERENCES restaurant.orders(id),
    menu_item_id INTEGER NOT NULL REFERENCES restaurant.menu_items(id),
	quantity INTEGER NOT NULL CHECK ( quantity > 0 ),
    price NUMERIC(10,2) NOT NULL CHECK (price > 0)
    );