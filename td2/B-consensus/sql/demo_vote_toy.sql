-- DEMO-VOTE : table jouet d'une seule ligne (donnees inventees, pas la base boutique)
-- Une vente du 2026-01-01, 100 centimes. Periode demandee : 1er janvier inclus -> 2 janvier exclu.
-- Reference attendue : 100.

-- Variante 1 (utilisee par 2 propositions sur 3) : borne basse EXCLUE par erreur
SELECT COALESCE(SUM(amount_cents), 0) AS revenue_cents
FROM sales
WHERE sale_date > '2026-01-01' AND sale_date < '2026-01-02';
-- => 0

-- Variante 2 (la 3e proposition) : borne basse incluse
SELECT COALESCE(SUM(amount_cents), 0) AS revenue_cents
FROM sales
WHERE sale_date >= '2026-01-01' AND sale_date < '2026-01-02';
-- => 100
