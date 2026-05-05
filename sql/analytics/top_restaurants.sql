-- top restauants by revenue, which makes the most money? 
-- windows func
-- r name and sum of all orders
-- 

SELECT
    restaurant.restaurants.name AS restaurant_name,
    SUM(restaurant.orders.total_price) AS total_revenue,
    COUNT(restaurant.orders.id) AS total_orders,
    RANK() OVER (ORDER BY SUM(restaurant.orders.total_price) DESC) AS revenue_rank
FROM restaurant.orders 
JOIN restaurant.restaurants ON restaurant.orders.restaurant_id = restaurant.restaurants.id
GROUP BY restaurant.restaurants.id, restaurant.restaurants.name
ORDER BY revenue_rank;