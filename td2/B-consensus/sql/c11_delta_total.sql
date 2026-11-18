-- Requete delta (2/2) : somme par client des lignes manquantes, puis total = ecart avec 0.
SELECT c.customer_id,
       c.birth_date,
       COUNT(*) AS nb_lignes,
       SUM(o.quantity_product * p.price) AS manquant_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE c.birth_date >  date('2026-12-01', '-26 years')
  AND c.birth_date <= date('2026-12-01', '-25 years')
GROUP BY c.customer_id, c.birth_date
ORDER BY c.birth_date;
