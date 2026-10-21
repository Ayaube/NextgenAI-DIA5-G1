-- C12 | product list
-- Question : What is the total revenue excluding VAT, in euro cents, of products a, b and c only, over all orders?
--
-- Auteur          : RASAKARAN Sharusan
-- Vérifié par     : Ayoub LAMCHICHI
-- Vérification    : calcul indépendant en Python pur sur les CSV (1666490)

-- Exécution (depuis la racine du repo) :
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C12.sql


SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON p.product_id = o.product_id
WHERE o.product_id IN ('a','b','c');

-- Résultat : revenue_cents = 1666490
