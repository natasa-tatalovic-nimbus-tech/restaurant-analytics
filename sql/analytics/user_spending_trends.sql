-- CTEs - user spending trends over time

WITH monthly_spending AS (
    SELECT
        u.id AS user_id,
        u.name,
        DATE_TRUNC('month', o.order_time) AS month,
        SUM(o.total_price) AS spent
    FROM restaurant.orders o
    JOIN restaurant.users u ON o.user_id = u.id
    GROUP BY u.id, u.name, DATE_TRUNC('month', o.order_time)
)
SELECT
    user_id,
    name,
    month,
    spent,
    LAG(spent) OVER (
        PARTITION BY user_id ORDER BY month
    ) AS previous_month_spent,
    spent - LAG(spent) OVER (
        PARTITION BY user_id ORDER BY month
    ) AS change
FROM monthly_spending
ORDER BY user_id, month;