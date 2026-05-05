SELECT
    DATE_TRUNC('month', order_time)    AS period,
    COUNT(*)                           AS order_count,
    SUM(total_price)                   AS revenue,
    AVG(total_price)                   AS avg_order_value
FROM restaurant.orders
GROUP BY period
ORDER BY period;