<<<<<<< HEAD
C18,"SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents 
FROM orders AS o 
JOIN customers AS c ON c.customer_id = o.customer_id 
JOIN product AS p ON p.product_id = o.product_id 
WHERE o.date >= '2026-05-01 00:00:00' AND o.date < '2026-06-01 00:00:00' AND CAST(substr(o.date, 1, 4) AS INTEGER) 
    - CAST(substr(c.birth_date, 1, 4) AS INTEGER) - (substr(o.date, 6, 5) < substr(c.birth_date, 6, 5)) = 25",62480
=======
-- C18 | period + age at the time of the order
-- Question : What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-05-01 00:00:00 to 2026-06-01 00:00:00 by customers who were exactly 25 years old at the time of the order?
--
-- Auteur          : Aurélien GL
-- Vérifié par     :
-- Vérification    : calcul indépendant sur customers.csv, orders.csv et product.csv
--
-- Conventions (consigne-etudiante-en.md, section 1) :
--   période    : date >= début AND date < fin
--   âge        : âge révolu au mois et au jour, jamais la seule différence d'années
--   montant    : SUM(quantity_product * price), centimes HT, 0 si rien (COALESCE)
--   sortie     : une ligne, une colonne nommée revenue_cents
-- Exécution (depuis la racine du repo) :
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C18.sql

-- Requête à écrire ici :
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-05-01 00:00:00'
  AND o.date < '2026-06-01 00:00:00'
  AND (
    CAST(strftime('%Y', o.date) AS INTEGER)
    - CAST(strftime('%Y', c.birth_date) AS INTEGER)
    - (strftime('%m-%d', o.date) < strftime('%m-%d', c.birth_date))
  ) = 25;

-- Résultat : revenue_cents = 62480
>>>>>>> a56c43e7b1d54ca25da242c0f9fb6b84e5d1a130
