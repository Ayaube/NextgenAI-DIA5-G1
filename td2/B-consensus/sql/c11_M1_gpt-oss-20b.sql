-- Query M1, openai/gpt-oss-20b (cas historique DEMO-SQL-C11), telle que renvoyee par le modele
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date = '2001-12-01';
