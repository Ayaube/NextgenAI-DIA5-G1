-- C17 | period + age on a reference date + product list
-- Question : What is the revenue excluding VAT, in euro cents, of products a, b and c only, for orders placed from 2026-01-01 00:00:00 to 2026-07-01 00:00:00 by customers who are exactly 25 years old on the reference date 2026-09-25?
--
-- Auteur          : Aurélien Guillout-Lacomblez
-- Vérifié par     : Maxence Tessier
-- Vérification    : calcul indépendant sur customers.csv, orders.csv et product.csv
--
-- Conventions (consigne-etudiante-en.md, section 1) :
--   période    : date >= début AND date < fin
--   âge        : âge révolu au mois et au jour, jamais la seule différence d'années
--   montant    : SUM(quantity_product * price), centimes HT, 0 si rien (COALESCE)
--   sortie     : une ligne, une colonne nommée revenue_cents
-- Exécution (depuis la racine du repo) :
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C17.sql

-- Requête à écrire ici :
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-01-01 00:00:00'
  AND o.date < '2026-07-01 00:00:00'
  AND o.product_id IN ('a', 'b', 'c')
  AND (
    CAST(strftime('%Y', '2026-09-25') AS INTEGER)
    - CAST(strftime('%Y', c.birth_date) AS INTEGER)
    - (strftime('%m-%d', '2026-09-25') < strftime('%m-%d', c.birth_date))
  ) = 25;

-- Résultat : revenue_cents = 258180
