-- Reference C11 (reference-td1.csv) : clients ayant exactement 25 ans au 2026-12-01
-- Fenetre de naissance : ]2000-12-01 ; 2001-12-01]
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE (2026 - CAST(substr(c.birth_date,1,4) AS INTEGER)) - ('12-01' < substr(c.birth_date,6,5)) = 25;
