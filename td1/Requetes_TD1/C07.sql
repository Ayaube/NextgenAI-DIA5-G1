-- C07 | period
-- Question : What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-05-31 00:00:00 to 2026-06-01 00:00:00?
--
-- Auteur          : Ayoub LAMCHICHI
-- Vérifié par     : hechmi Chemli
-- Vérification    : somme sur les CSV (3*2990 + 4*1250) = 13970.

SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p USING (product_id)
WHERE o.date >= '2026-05-31 00:00:00'
  AND o.date <  '2026-06-01 00:00:00';

-- Résultat : revenue_cents = 13970
