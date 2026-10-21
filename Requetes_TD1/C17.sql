-- C17 | period + age on a reference date + product list
-- Question : What is the revenue excluding VAT, in euro cents, of products a, b and c only, for orders placed from 2026-01-01 00:00:00 to 2026-07-01 00:00:00 by customers who are exactly 25 years old on the reference date 2026-09-25?
--
-- Auteur          :
-- Vérifié par     :
-- Vérification    : (méthode indépendante : autre requête, calcul sur les CSV...)
--
-- Conventions (consigne-etudiante-en.md, section 1) :
--   période    : date >= début AND date < fin
--   âge        : âge révolu au mois et au jour, jamais la seule différence d'années
--   montant    : SUM(quantity_product * price), centimes HT, 0 si rien (COALESCE)
--   sortie     : une ligne, une colonne nommée revenue_cents
-- Exécution (depuis la racine du repo) :
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C17.sql

-- Requête à écrire ici :


-- Résultat : revenue_cents =
