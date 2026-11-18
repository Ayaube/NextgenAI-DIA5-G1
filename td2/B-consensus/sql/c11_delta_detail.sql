-- Requete delta (1/2) : les lignes de commande comptees par la reference mais pas par M1 ni M2.
-- Pour chaque ligne : le client, sa date de naissance, la commande, le CA hors TVA de la ligne,
-- et deux colonnes qui disent si M1 / M2 auraient garde la ligne dans leur WHERE.
SELECT c.customer_id,
       c.birth_date,
       o.order_id,
       o.product_id,
       o.quantity_product * p.price AS ligne_cents,
       (c.birth_date = '2001-12-01') AS gardee_par_M1,
       ('2026-12-01' >= c.birth_date AND '2027-12-01' <= c.birth_date) AS gardee_par_M2
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE c.birth_date >  date('2026-12-01', '-26 years')   -- 2000-12-01 exclu
  AND c.birth_date <= date('2026-12-01', '-25 years')   -- 2001-12-01 inclus
ORDER BY c.customer_id, o.order_id, o.product_id;
