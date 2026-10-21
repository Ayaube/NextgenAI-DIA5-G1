-- C20 | period
-- Question : What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-06-01 00:00:00 to 2026-09-01 00:00:00?
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
--   sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C20.sql

-- Requête à écrire ici :


-- Résultat : revenue_cents =
