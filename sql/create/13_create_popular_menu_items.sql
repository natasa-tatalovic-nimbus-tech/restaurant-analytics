CREATE TABLE IF NOT EXISTS analytics.popular_menu_items (
    menu_item_id INTEGER REFERENCES restaurant.menu_items(id),
    name VARCHAR(100),
    restaurant_id INTEGER,
    total_quantity INTEGER,
    total_revenue NUMERIC(10,2),
    revene_rank INTEGER
);