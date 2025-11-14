
SELECT
  o.user_id,
  u.username,
  o.order_id,
  o.order_date,
  oi.product_id,
  p.name AS product_name,
  oi.quantity,
  oi.unit_price,
  COALESCE(r.avg_rating, 0) AS product_avg_rating
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN (
  SELECT product_id, AVG(rating) AS avg_rating
  FROM reviews
  GROUP BY product_id
) r ON oi.product_id = r.product_id
WHERE o.order_date >= datetime('now', '-30 day')
ORDER BY o.order_date DESC;
