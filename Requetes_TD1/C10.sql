-- C10 | age at the time of the order
-- Question : What is the total revenue excluding VAT, in euro cents, of the orders placed by customers who were exactly 25 years old at the time of the order?
--
-- Auteur          : Sharusan Rasakaran
-- Vérifié par     : Ayoub
-- Vérification    : calcul indépendant en Python pur sur les CSV (data/orders.csv, customers.csv, product.csv),
--                   sans SQL
--
-- Exécution (depuis la racine du repo) :
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C10.sql


SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE (CAST(substr(o.date,1,4) AS INTEGER) - CAST(substr(c.birth_date,1,4) AS INTEGER))
      - (substr(o.date,6,5) < substr(c.birth_date,6,5)) = 25;

-- Résultat : revenue_cents = 558980
