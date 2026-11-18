# TD 2 - Pair B : le wrong consensus (Step 2)

Section de la Pair B pour `reports/td2.md` (à recopier dans le rapport commun au moment de l'assemblage).
Tous les chiffres ci-dessous viennent de scripts du dossier `B-consensus/`, à lancer depuis la racine du repo.

| Fichier | Rôle |
|---|---|
| `B-consensus/01_valeurs_fausses_partagees.py` | cherche les valeurs fausses partagées dans `B-consensus/traces-td1.csv` |
| `B-consensus/03_c11_demo.py` | DEMO-VOTE, M1, M2, requête delta, vérification indépendante |
| `B-consensus/04_quorum_pairB.py` | comptage des votes 2-sur-3 et 3-sur-5 |
| `B-consensus/sql/*.sql` | toutes les requêtes SQL utilisées |

## 1. Recherche dans nos 100 cellules

`B-consensus/traces-td1.csv` contient 105 lignes : 5 lignes en trop sont des tentatives de Qwen rejouées après un HTTP 429 (colonne `attempts`).
En gardant la dernière tentative de chaque couple (modèle, question), on obtient bien 100 cellules :
82 `correct`, 14 `incorrect`, 2 `sql_invalid` (North C02, Dots C19), 2 `not_executed` (Qwen C16 et C18, toujours en 429).

Les 14 valeurs fausses sont :

| Question | Modèle | Valeur fausse | Référence |
|---|---|---|---|
| C02 | gpt-oss-20b | 0 | 590320 |
| C08 | north-mini-code | 0 | 605580 |
| C09 | north-mini-code | 0 | 487980 |
| C09 | dots-3 | 134660 | 487980 |
| C10 | north-mini-code | 548920 | 558980 |
| C11 | north-mini-code | 0 | 446690 |
| C15 | qwen3.8-27b | 0 | 168680 |
| C15 | dots-3 | 138920 | 168680 |
| C16 | dots-3 | 211260 | 376740 |
| C17 | north-mini-code | 105840 | 258180 |
| C17 | dots-3 | 152730 | 258180 |
| C17 | qwen3.8-27b | 248490 | 258180 |
| C18 | dots-3 | 39580 | 62480 |
| C19 | qwen3.8-27b | 83580 | 1990 |

**Résultat : aucune valeur fausse partagée.** Sur une même question, deux modèles qui se trompent donnent deux valeurs différentes
(C09, C15 et C17 ont même 2 ou 3 valeurs fausses distinctes). La valeur 0 revient souvent, mais jamais sur la même question
avec deux modèles différents : C02, C08, C09, C11 et C15 ont chacune un seul modèle à 0.
Comme l'énoncé le prévoit, on prend donc le cas historique **DEMO-SQL-C11** (septembre 2026), et on le dit clairement :
**c'est un cas rejoué, pas un cas de notre lot.** Dans notre lot, C11 est correct pour 4 modèles sur 5 (seul North rend 0).

## 2. DEMO-VOTE : le mécanisme sur la table jouet (données inventées)

Une vente du 2026-01-01 de 100 centimes. Période demandée : du 1er janvier inclus au 2 janvier exclu. Référence : 100.

- `sale_date > '2026-01-01' AND sale_date < '2026-01-02'` rend **0** (la vente du 1er janvier à 00:00 est exclue par le `>`). Deux propositions l'utilisent.
- `sale_date >= '2026-01-01' AND sale_date < '2026-01-02'` rend **100**. Une proposition l'utilise.

Propositions `[0, 0, 100]`, seuil 2 sur 3 : la valeur 0 a 2 voix, elle gagne, alors que la référence est 100.
Le vote ne regarde que l'accord entre les modèles, pas la vérité : deux modèles qui partagent le même défaut gagnent.
(Résultat obtenu en exécutant les deux requêtes dans `03_c11_demo.py` et en comptant avec `04_quorum_pairB.py`.)

## 3. Cas DEMO-SQL-C11

### 3.1 Identification

- Question : **C11**, CA hors TVA en centimes des clients qui ont exactement 25 ans au 2026-12-01, sur toutes leurs commandes.
- Modèles d'accord sur la valeur fausse : `openai/gpt-oss-20b` (Groq, requête M1) et `cohere/north-mini-code:free` (OpenRouter, requête M2).
- Valeur fausse partagée : **0**. Valeur de référence (`reference-td1.csv`) : **446690** centimes.
- Nature : cas historique du pilote de septembre 2026, **rejoué** sur `data/boutique.sqlite`. Les requêtes M1 et M2 sont celles de l'énoncé.
  Les deux tournent sans erreur et rendent bien 0 sur la base (vérifié dans `03_c11_demo.py`).

### 3.2 Les deux requêtes fautives

```sql
-- M1, openai/gpt-oss-20b
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date = '2001-12-01';

-- M2, cohere/north-mini-code:free
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE CAST(strftime('%Y-%m-%d', '2026-12-01') AS TEXT) >= c.birth_date
  AND CAST(strftime('%Y-%m-%d', '2026-12-01', '+1 year') AS TEXT) <= c.birth_date;
```

### 3.3 Quelle fenêtre de naissance chaque `WHERE` teste

"Exactement 25 ans au 2026-12-01" veut dire : être né après le 2000-12-01 (sinon on a déjà 26 ans) et au plus tard le 2001-12-01
(sinon on n'a pas encore 25 ans). La fenêtre exacte est donc **]2000-12-01 ; 2001-12-01]**. Elle contient 6 clients dans la base.

- **M1** : `birth_date = '2001-12-01'` ne teste qu'**un seul jour**, le dernier de la fenêtre (le client qui fête ses 25 ans pile ce jour-là).
  Personne n'est né ce jour-là dans la base (0 client), donc le `JOIN` ne produit aucune ligne.
- **M2** : les deux conditions disent `birth_date <= '2026-12-01'` **et** `birth_date >= '2027-12-01'`. Il faudrait être né
  avant fin 2026 et après fin 2027 en même temps : l'intervalle est **vide**, aucun client ne peut le satisfaire (0 client dans la base).
  Le modèle a ajouté 1 an à la date de référence au lieu de la reculer de 25 et 26 ans, et le sens des comparaisons est inversé.
  Les `CAST(... AS TEXT)` ne servent à rien (`strftime` rend déjà du texte).
- Dans les deux cas, aucune ligne n'est sélectionnée, `SUM` rend `NULL` et `COALESCE(..., 0)` le transforme en **0**.
  C'est ce `COALESCE` qui rend l'erreur silencieuse : on obtient un nombre d'apparence normale et pas d'erreur SQL.

Les deux modèles ont fait deux bugs différents, mais qui mènent au même résultat (ensemble vide, donc 0).
Ils sont d'accord sans avoir raison, et sans qu'aucune erreur ne se déclenche.

### 3.4 Verdict des quorums

Pour 2-sur-3 et 3-sur-5, on déclare le panel et le seuil à chaque fois. Les valeurs des trois autres modèles (120B, Qwen, Dots)
sont celles de nos traces réelles pour C11 (446690 pour les trois). **Ce scénario est donc reconstitué** : on suppose que ces trois modèles
auraient rendu leur valeur actuelle lors du pilote de septembre.

| Quorum | Panel (n) | k | Valeurs | Résultat |
|---|---|---|---|---|
| 2-sur-3, panel fixe de `atelier-vote.py` | 120B, North, Qwen | 2 | 446690, **0**, 446690 | consensus **446690** (2 voix), le 0 n'a qu'1 voix : **vote juste** |
| 2-sur-3, autre panel (hypothèse) | 20B, North, 120B | 2 | **0**, **0**, 446690 | consensus **0** (2 voix) : **wrong consensus** |
| 3-sur-5, les 5 modèles | 120B, North, Qwen, 20B, Dots | 3 | 446690, 0, 446690, 0, 446690 | consensus **446690** (3 voix), le 0 n'a que 2 voix : **vote juste** |
| 3-sur-5, contre-exemple (hypothèse) | les 5 | 3 | Qwen aurait aussi rendu 0 | consensus **0** (3 voix) : **wrong consensus** |

Dans le panel fixe, le wrong consensus ne peut pas se produire parce que seul North y figure (20B n'est pas dans le panel).
Il suffit pourtant que le panel contienne les deux modèles fautifs pour que 2-sur-3 se trompe, et 3-sur-5 ne protège que tant
qu'au plus 2 modèles sur 5 partagent le défaut.

Sur **nos traces réelles** de C11 : 2-sur-3 rend 446690 (120B et Qwen), 3-sur-5 rend 446690 (4 voix : 120B, Qwen, 20B, Dots), North est battu avec son 0.
Sur l'ensemble des 20 questions, ni 2-sur-3 ni 3-sur-5 n'a de wrong consensus ; les deux s'abstiennent sur C17
(2-sur-3 : trois valeurs différentes, 258180 / 105840 / 248490 ; 3-sur-5 : 258180 n'a que 2 voix, contre 3 valeurs fausses toutes différentes).

Remarque sur le 20B dans nos traces : il rend bien 446690 sur C11, mais avec `birth_date BETWEEN '2001-01-01' AND '2001-12-01'`.
Cette fenêtre est fausse en théorie (elle oublie les clients nés entre le 2000-12-02 et le 2000-12-31). Elle ne donne le bon chiffre
que parce que la base n'a aucun client né sur cette période (vérifié : 0). C'est un cas "juste pour une mauvaise raison", ce qui montre
qu'un `correct` dans le tableau ne prouve pas que la requête est bonne sur une autre base.

## 4. Requête delta sur `data/boutique.sqlite`

Fichiers : `B-consensus/sql/c11_delta_detail.sql` et `B-consensus/sql/c11_delta_total.sql`. Elles listent exactement les lignes de commande
comptées par la référence (fenêtre `]2000-12-01 ; 2001-12-01]`) et rejetées par M1 et par M2 (colonnes `gardee_par_M1` et `gardee_par_M2` : 0 sur toutes les lignes).

```sql
SELECT c.customer_id, c.birth_date,
       COUNT(*) AS nb_lignes,
       SUM(o.quantity_product * p.price) AS manquant_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE c.birth_date >  date('2026-12-01', '-26 years')
  AND c.birth_date <= date('2026-12-01', '-25 years')
GROUP BY c.customer_id, c.birth_date
ORDER BY c.birth_date;
```

Résultat exécuté (60 lignes de commande au détail, 6 clients) :

| customer_id | birth_date | lignes | CA manquant (centimes) |
|---|---|---|---|
| C009 | 2001-03-10 | 9 | 61330 |
| C008 | 2001-05-15 | 11 | 99090 |
| C002 | 2001-09-24 | 6 | 25920 |
| C001 | 2001-09-25 | 18 | 135000 |
| C003 | 2001-09-26 | 6 | 47900 |
| C006 | 2001-11-30 | 10 | 77450 |
| **Total** | | **60** | **446690** |

Le total vaut exactement la référence C11 (446690). Comme M1 et M2 rendent 0, **l'écart de 446690 centimes est entièrement expliqué
par ces 6 clients** : aucun n'est né le 2001-12-01 (M1) et aucun ne tombe dans l'intervalle vide de M2.

## 5. Méthode de vérification indépendante

`03_c11_demo.py` recalcule le résultat **sans SQL** : lecture de `data/customers.csv`, `data/orders.csv` et `data/product.csv`,
calcul de l'âge au 2026-12-01 avec des dates Python (année moins année, moins 1 si l'anniversaire n'est pas encore passé),
puis somme de `quantité x prix` des commandes des clients de 25 ans. Résultat : 6 clients, **446690**, identique à la référence et à la requête delta.
Le comptage des votes de ce document est fait par `04_quorum_pairB.py` avec une fonction `vote` écrite par nous.
**À recouper avec la méthode `Orchestrateur.vote_k_sur_n` de la Pair A dès qu'elle est livrée** (mêmes entrées : seuil strict, un modèle indisponible reste dans n, pas de doublon).

## 6. Conséquence pour le contrôle

- Un vote majoritaire protège contre une erreur isolée (North à 0 est battu), mais pas contre un défaut **partagé** :
  M1 et M2 sont deux bugs différents qui donnent le même résultat vide, et 2-sur-3 les valide s'ils sont tous deux dans le panel.
- Une valeur 0 est un résultat légitime (C06 et C14 valent 0 dans la référence), donc on ne peut pas rejeter tous les 0.
  Un contrôle déterministe peut en revanche vérifier **combien de clients ou de lignes le filtre a sélectionnés** : un filtre "25 ans" qui n'en sélectionne aucun
  alors qu'il en existe 6 est suspect. Pour un montant versé ou un chiffre montré au client, cela justifie une requête de référence ou une relecture
  plutôt qu'un simple quorum (hypothèse à discuter avec la Pair C pour la règle de routage ; un seul cas ne suffit pas à fixer un taux d'erreur).
- Limite : 20 questions et une seule base, donc ceci illustre un mécanisme sans mesurer une fréquence.

## 7. Limites et honnêteté

- Cas **rejoué** : C11 historique, pas une observation de notre lot. Les scénarios "panel 20B/North/120B" et "Qwen à 0" sont des hypothèses.
- Les requêtes M1 et M2 sont reproduites telles que données dans l'énoncé.
- Ce document et les scripts ont été préparés avec l'aide d'un assistant IA (Claude), puis exécutés sur la base. À déclarer aussi dans `ai-assistance.md`.
- Comptage "à la main" à valider par les deux membres de la Pair B, et à confronter à la méthode de la Pair A.
