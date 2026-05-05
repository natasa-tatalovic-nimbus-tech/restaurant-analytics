CREATE TABLE IF NOT EXISTS analytics.user_order_summary (
    user_id      INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL, 
	email VARCHAR(100) NOT NULL UNIQUE,
    total_orders  INTEGER NOT NULL DEFAULT 0, -- how much is u ordering 
    total_spent   NUMERIC(10, 2) NOT NULL DEFAULT 0.00 -- money spent
);
