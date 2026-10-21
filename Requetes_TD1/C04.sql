-- C04 | period
-- Question : What is the total revenue excluding VAT, in euro cents, of the orders placed from 2026-01-01 00:00:00 to 2026-10-01 00:00:00?
--
-- Auteur          : hechmi Chemli
-- Vérifié par     : Aurelien Roche
-- Vérification    : (méthode indépendante : autre requête, calcul sur les CSV...)
--
-- Conventions (consigne-etudiante-en.md, section 1) :
--   période    : date >= début AND date < fin
--   âge        : âge révolu au mois et au jour, jamais la seule différence d'années
--   montant    : SUM(quantity_product * price), centimes HT, 0 si rien (COALESCE)
--   sortie     : une ligne, une colonne nommée revenue_cents
-- Exécution (depuis la racine du repo) :
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C04.sql

-- Requête à écrire ici :

SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
WHERE o.date >= '2026-01-01 00:00:00'
  AND o.date < '2026-10-01 00:00:00';

-- Résultat : revenue_cents = 2 826 250
