C19,"SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents 
FROM orders AS o 
JOIN customers AS c ON c.customer_id = o.customer_id 
JOIN product AS p ON p.product_id = o.product_id 
WHERE o.date >= '2026-09-01 00:00:00' AND o.date < '2026-10-01 00:00:00' AND o.product_id = 'd' AND 2026 
    - CAST(substr(c.birth_date, 1, 4) AS INTEGER) - ('09-25' < substr(c.birth_date, 6, 5)) = 25",1990

    -- Vérifié par     : Aurélien GL