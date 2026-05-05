CREATE TABLE IF NOT EXISTS analytics.dim_menu_items (
    menu_item_key   SERIAL PRIMARY KEY,
    menu_item_id    INTEGER NOT NULL,
    restaurant_id   INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2)  NOT NULL
);