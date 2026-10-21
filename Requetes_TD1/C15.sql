-- C15 | period + age on a reference date
-- Question : What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-03-01 00:00:00 to 2026-06-01 00:00:00 by customers who are exactly 25 years old on the reference date 2026-09-25?
--
-- Auteur          : Jérémie LEROY-DUBIEF
-- Vérifié par     : RASAKARAN Sharusan
-- Vérification    : (méthode indépendante : autre requête, calcul sur les CSV...)
--
-- Conventions (consigne-etudiante-en.md, section 1) :
--   période    : date >= début AND date < fin
--   âge        : âge révolu au mois et au jour, jamais la seule différence d'années
--   montant    : SUM(quantity_product * price), centimes HT, 0 si rien (COALESCE)
--   sortie     : une ligne, une colonne nommée revenue_cents
-- Exécution (depuis la racine du repo) :
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C15.sql

-- Requête à écrire ici :
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
        FROM orders o
        JOIN product p   ON p.product_id   = o.product_id
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE o.date >= '2026-03-01 00:00:00' AND o.date < '2026-06-01 00:00:00'
          AND (CAST(strftime('%Y', '2026-09-25') AS INTEGER)
               - CAST(strftime('%Y', c.birth_date) AS INTEGER)
               - (strftime('%m-%d', '2026-09-25') < strftime('%m-%d', c.birth_date))) = 25;

-- Résultat : revenue_cents = 168680
