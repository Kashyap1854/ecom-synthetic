WITH recent_orders AS (
  SELECT o.order_id, o.user_id, o.order_date
  FROM orders o
  WHERE datetime(o.order_date) >= datetime('now', '-30 days')
),
items_with_products AS (
  SELECT oi.order_item_id, oi.order_id, oi.product_id, oi.quantity, oi.unit_price, p.name as product_name
  FROM order_items oi
  JOIN products p ON p.product_id = oi.product_id
),
product_avg_rating AS (
  SELECT product_id, AVG(rating) AS avg_rating
  FROM reviews
  GROUP BY product_id
)
SELECT
  ro.user_id,
  u.username,
  ro.order_id,
  ro.order_date,
  iw.product_id,
  iw.product_name,
  iw.quantity,
  iw.unit_price,
  COALESCE(par.avg_rating, 0) AS product_avg_rating
FROM recent_orders ro
JOIN users u ON u.user_id = ro.user_id
JOIN items_with_products iw ON iw.order_id = ro.order_id
LEFT JOIN product_avg_rating par ON par.product_id = iw.product_id
ORDER BY ro.order_date DESC, ro.user_id;