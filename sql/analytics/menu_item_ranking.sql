-- Windows function mostly used for rankings
-- Top restaurants by revenue
SELECT
    mi.name AS item_name,
    r.name AS restaurant_name,
    SUM(oi.quantity * oi.price) AS total_revenue,
    SUM(oi.quantity) AS total_quantity,
    RANK() OVER (
        ORDER BY SUM(oi.quantity * oi.price) DESC
    ) AS revenue_rank,
    DENSE_RANK() OVER (
        ORDER BY SUM(oi.quantity) DESC
    ) AS popularity_rank
FROM restaurant.order_items oi
JOIN restaurant.menu_items mi ON oi.menu_item_id = mi.id
JOIN restaurant.restaurants r ON mi.restaurant_id = r.id
GROUP BY mi.id, mi.name, r.id, r.name
ORDER BY revenue_rank;  