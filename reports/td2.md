# TD 2 : le quorum, puis la règle de routage

Sous-groupe DIA5-G1, séance du 18 novembre 2026, pack 2026-11-18-students-5.

Tout ce rapport repose sur les traces réelles du TD 1, dans td1/traces-td1.csv, et sur notre référence td1/reference-td1.csv. Aucun nouvel appel à un fournisseur n'a été fait. Les exemples synthétiques et le cas rejoué sont signalés là où ils apparaissent.

## Ce qui a été fait

- Partie A : la méthode vote_k_sur_n est complétée et testée. Le panel 2 sur 3 et le quorum 3 sur 5 ont été comparés sur les vingt questions. Détail dans [td2/A-quorum/rapport-A.md](../td2/A-quorum/rapport-A.md).
- Partie B : aucune valeur fausse n'est partagée dans nos traces. Le cas historique C11 a été rejoué et expliqué en SQL, avec la requête qui isole tout l'écart. Détail dans [td2/B-consensus/rapport-B.md](../td2/B-consensus/rapport-B.md).
- Partie C : la règle de routage est écrite famille par famille, à partir des taux du TD 1. Le simulateur est adapté et ses sorties sont gardées avant et après. Détail dans [td2/C-routing/regle-routage.md](../td2/C-routing/regle-routage.md).

Les prompts n'ont pas changé depuis le TD 1.

## Étape 1 : le vote k sur n

La méthode ne fait voter que les propositions exécutées qui ont une valeur. Une erreur ou une indisponibilité reste comptée dans n mais ne vote pas. Le seuil k doit être une majorité stricte, sinon la méthode refuse. Deux propositions du même fournisseur et du même modèle sont refusées. Si une valeur atteint k voix, elle est gardée. Sinon la méthode s'abstient et ne renvoie aucune valeur. La référence n'intervient qu'après la décision.

Les quatre exemples synthétiques du kit donnent le résultat attendu : accord gardé, désaccord en abstention, indisponibilité en abstention, et le faux consensus [0, 0, 100] qui garde 0. Les huit tests passent, voir [tests.txt](../td2/A-quorum/tests.txt).

Le panel 2 sur 3 est fixe : gpt-oss-120b et qwen3.8-27b sur Groq, north-mini-code sur OpenRouter. Le quorum 3 sur 5 ajoute gpt-oss-20b et dots-3-note. Pour chaque modèle, on prend sa dernière tentative sur la question.

| Question | Référence | 2 sur 3 | Voix | 3 sur 5 | Voix | Accord avec la référence |
|---|---:|---|---:|---|---:|---|
| C01 | 792800 | 792800 | 3 | 792800 | 5 | oui, oui |
| C02 | 590320 | 590320 | 2 | 590320 | 3 | oui, oui |
| C03 | 936350 | 936350 | 3 | 936350 | 5 | oui, oui |
| C04 | 2826250 | 2826250 | 3 | 2826250 | 5 | oui, oui |
| C05 | 38480 | 38480 | 3 | 38480 | 5 | oui, oui |
| C06 | 0 | 0 | 3 | 0 | 5 | oui, oui |
| C07 | 13970 | 13970 | 3 | 13970 | 5 | oui, oui |
| C08 | 605580 | 605580 | 2 | 605580 | 4 | oui, oui |
| C09 | 487980 | 487980 | 2 | 487980 | 3 | oui, oui |
| C10 | 558980 | 558980 | 2 | 558980 | 4 | oui, oui |
| C11 | 446690 | 446690 | 2 | 446690 | 4 | oui, oui |
| C12 | 1666490 | 1666490 | 3 | 1666490 | 5 | oui, oui |
| C13 | 107740 | 107740 | 3 | 107740 | 5 | oui, oui |
| C14 | 0 | 0 | 3 | 0 | 5 | oui, oui |
| C15 | 168680 | 168680 | 2 | 168680 | 3 | oui, oui |
| C16 | 376740 | 376740 | 2 | 376740 | 3 | oui, oui |
| C17 | 258180 | abstention | 1 | abstention | 2 | sans réponse dans les deux cas |
| C18 | 62480 | 62480 | 2 | 62480 | 3 | oui, oui |
| C19 | 1990 | 1990 | 2 | 1990 | 3 | oui, oui |
| C20 | 1106090 | 1106090 | 3 | 1106090 | 5 | oui, oui |

Bilan : 19 valeurs justes, aucun faux consensus et une abstention dans les deux votes. Passer de 2 sur 3 à 3 sur 5 ne change aucune décision sur nos traces. Le CSV complet est [comparaison-quorums.csv](../td2/A-quorum/comparaison-quorums.csv).

Ce qui change, c'est la marge au-dessus du seuil.

- C17 : dans le panel, les trois valeurs sont différentes, 258180 pour 120B, 105840 pour Cohere et 248490 pour Qwen. Dans le quorum, 258180 a deux voix, 120B et 20B, et il en faut trois. Dots donne 152730. Les deux votes s'abstiennent, ce qui est le bon comportement : ils ne fabriquent pas de valeur.
- C16 et C18 : Qwen est non exécuté après deux erreurs HTTP 429. Il reste dans n sans voter. Le panel garde la bonne valeur avec 120B et Cohere. Le quorum l'atteint tout juste avec trois voix, car Dots se trompe (211260 sur C16, 39580 sur C18).
- C19 : Dots a un SQL invalide et ne vote pas, Qwen donne 83580. Le quorum passe tout juste avec 120B, 20B et Cohere.
- C02 : Cohere a un SQL invalide et 20B donne 0. Le quorum passe tout juste avec 120B, Qwen et Dots.
- C09 et C15 : deux valeurs fausses et différentes sur chaque question, et le quorum passe tout juste avec trois voix.

Sur six questions, C02, C09, C15, C16, C18 et C19, le quorum 3 sur 5 est exactement au seuil. Une panne de plus, un 429 par exemple, le ferait passer en abstention. Le quorum plus large demande plus de voix, donc il est plus exposé aux pannes d'accès.

## Étape 2 : le faux consensus

Nos cent cellules contiennent quatorze valeurs fausses, mais jamais la même valeur fausse pour deux modèles sur une même question. Sur C09, C15 et C17, les modèles qui se trompent donnent tous des valeurs différentes. On a donc pris le cas historique DEMO-SQL-C11 du sujet. C'est un cas rejoué, pas une observation de notre lot.

Question C11 : le chiffre d'affaires hors TVA, en centimes, des clients qui ont exactement 25 ans le 2026-12-01. Lors du pilote de septembre 2026, gpt-oss-20b et north-mini-code ont rendu deux requêtes différentes. Les deux renvoient 0 sur la base. Notre référence vaut 446690.

La requête de gpt-oss-20b filtre sur birth_date = '2001-12-01'. Elle ne garde qu'un seul jour, le dernier de la bonne fenêtre, et aucun client n'est né ce jour-là.

La requête de north-mini-code demande une date de naissance inférieure ou égale au 2026-12-01 et supérieure ou égale au 2027-12-01. Aucune date ne remplit les deux conditions.

Dans les deux cas, aucune ligne n'est retenue, la somme est vide et COALESCE la transforme en 0. L'erreur est silencieuse : le résultat ressemble à un vrai montant.

La bonne fenêtre est une naissance après le 2000-12-01 et au plus tard le 2001-12-01. La requête suivante, exécutée sur td1/data/boutique.sqlite, liste les clients comptés par la référence et oubliés par les deux requêtes fautives.

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

| Client | Naissance | Lignes | Montant manquant |
|---|---|---:|---:|
| C009 | 2001-03-10 | 9 | 61330 |
| C008 | 2001-05-15 | 11 | 99090 |
| C002 | 2001-09-24 | 6 | 25920 |
| C001 | 2001-09-25 | 18 | 135000 |
| C003 | 2001-09-26 | 6 | 47900 |
| C006 | 2001-11-30 | 10 | 77450 |
| Total | | 60 | 446690 |

Le total est exactement la référence. Ces six clients expliquent donc tout l'écart entre 0 et 446690. Un second calcul en Python, sans SQL, à partir des CSV de la base, trouve aussi six clients et 446690.

Verdict des votes. Dans le panel fixe, seul Cohere fait partie des deux modèles fautifs. Avec 120B et Qwen à 446690, le 0 n'a qu'une voix et perd. Dans le quorum 3 sur 5, le 0 a deux voix, celles de 20B et de Cohere, et 446690 en a trois, celles de 120B, Qwen et Dots. Le 0 perd encore. Ce scénario est reconstitué : on suppose que les trois autres modèles auraient rendu leur valeur de nos traces. Si le panel avait contenu 20B et Cohere, le 2 sur 3 aurait gardé 0. Un vote protège contre une erreur isolée, pas contre un défaut partagé.

Sur nos propres traces de C11, seul Cohere rend 0. Les deux votes gardent 446690.

Conséquence pour le contrôle : 0 peut être une vraie réponse, puisque C06 et C14 valent 0. On ne peut donc pas rejeter tous les 0. On peut en revanche vérifier combien de clients le filtre a retenus. Un filtre sur les 25 ans qui ne retient personne alors que six clients existent doit alerter. Pour un montant montré au client ou versé, un quorum ne suffit pas, il faut une requête de référence indépendante.

## Étape 3 : la règle de routage

Taux exacts du TD 1, en réponses justes sur cas, par modèle et par famille. Le détail des cellules est dans [regle-routage.md](../td2/C-routing/regle-routage.md).

| Famille | Cellules | 120B | 20B | Qwen | Cohere | Dots |
|---|---|---|---|---|---|---|
| F1 période | C01, C04, C05, C06, C07, C20 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| F2 âge à une date | C02, C08, C09, C11 | 4/4 | 3/4 | 4/4 | 0/4 | 3/4 |
| F2b âge à la commande | C10 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 |
| F3 liste de produits | C03, C12, C13, C14 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| F4 combinaisons | C15 à C19 | 5/5 | 5/5 | 0/5 | 4/5 | 0/5 |

Sur F4, deux des cinq échecs de Qwen sont des refus d'accès (HTTP 429 sur C16 et C18), pas des mauvaises réponses. Les cinq modèles sont gratuits sur les routes utilisées. Ce qui les sépare, ce sont les quotas et l'existence d'une route payante de secours, qui n'est documentée que pour gpt-oss-120b sur OpenRouter.

La règle, en une page :

- F1 période. Premier modèle : gpt-oss-20b, le plus petit, juste sur 6/6. Tableau interne : ce modèle seul, avec exécution en lecture seule et contrôle d'un entier en centimes. Chiffre client : vote 2 sur 3 entre 20B, Cohere et Dots. Montant versé : comparaison avec la requête de référence, puis relecture humaine.
- F2 âge à une date. Premier modèle : gpt-oss-120b, juste sur 4/4. Tableau interne : 120B seul. Chiffre client : vote 2 sur 3 entre 120B, Qwen et Dots, sans Cohere qui fait 0/4. Montant versé : référence indépendante et relecture humaine. Le cas C11 montre qu'un quorum seul ne suffit pas sur cette famille.
- F2b âge à la commande. Premier modèle : gpt-oss-120b, juste sur C10 et sur toute la famille F2, qui utilise la même règle d'âge. Chiffre client : vote 2 sur 3 entre 120B, Qwen et Dots. Montant versé : comparaison avec td1/Requetes_TD1/C10.sql et relecture.
- F3 liste de produits. Premier modèle : gpt-oss-20b, juste sur 4/4, ce qui garde les quotas de 120B et Qwen pour F2 et F4. Chiffre client : vote 2 sur 3 entre 120B, Cohere et Qwen. Montant versé : référence indépendante.
- F4 combinaisons. Premier modèle : gpt-oss-120b, l'un des deux seuls modèles justes sur 5/5. Chiffre client : vote 2 sur 3 entre 120B, Cohere et Qwen. Montant versé : référence indépendante.

Si le premier modèle est indisponible, on suit cet ordre : capacité déjà payée si elle existe, puis un autre modèle gratuit juste à 100 % sur la famille, de préférence chez l'autre fournisseur. Ensuite, attente de la recharge si la demande peut attendre, puis gpt-oss-120b payant sur OpenRouter dans la limite du budget, puis abstention. On ne retombe jamais sur un modèle seul qui a fait une erreur sur la famille. On s'arrête à dix appels gratuits par demande. Le contrôle exigé ne change pas quand on change de route.

Vingt questions donnent une hypothèse propre à notre lot, pas un taux d'erreur général ni un classement définitif.

## Le simulateur, avant et après

Avant adaptation, avec les trois ressources fictives du kit ([simulateur-avant.txt](../td2/C-routing/simulateur-avant.txt)) :

| Scénario | Décision | Ressource | Raison |
|---|---|---|---|
| simple | exécuter | small-free | capacité incluse éligible |
| complex | exécuter | senior-subscription | capacité incluse éligible |
| deferrable | différer de 60 min | senior-subscription | revérifier au réveil |
| urgent | exécuter | senior-api, 0,30 USD | route disponible dans le budget |
| budget exhausted | s'abstenir | aucune | rien d'éligible dans le délai et le budget |
| high impact | exécuter | senior-subscription | capacité incluse, avec vérification de la source et relecture humaine |
| unknown capability | s'abstenir | aucune | aucune ressource de niveau 4 |

Après adaptation, avec nos cinq routes gratuites et la route payante de gpt-oss-120b ([simulateur-apres.txt](../td2/C-routing/simulateur-apres.txt), code dans [atelier-routage.py](../td2/C-routing/atelier-routage.py)) :

| Scénario | Décision | Ressource | Raison citée |
|---|---|---|---|
| simple | exécuter | gpt-oss-20b sur Groq | F1, cellules C01, C04, C05, C06, C07, C20 |
| complex | exécuter | gpt-oss-120b sur Groq | F4, cellules C15 à C19 |
| deferrable | différer de 60 min | gpt-oss-120b sur Groq | F4, les deux routes gratuites éligibles sont indisponibles |
| urgent | exécuter | gpt-oss-120b sur OpenRouter, environ 0,000285 USD | F4, la route payante tient dans le budget |
| budget exhausted | s'abstenir | aucune | F4, rien d'éligible dans le délai et le budget |
| high impact | exécuter | gpt-oss-120b sur Groq | F4, avec égalité exacte en centimes contre une référence indépendante |
| unknown capability | s'abstenir | aucune | aucune preuve du TD 1 pour cette famille |

Le coût payant suppose 1 500 jetons en entrée et 100 en sortie, aux prix du portefeuille du 28 septembre 2026.

## L'ordre de priorité dans choose

Dans la fonction choose fournie, la première branche cherche une ressource éligible, disponible et sans dépense supplémentaire, avec cash égal à 0. Un abonnement disponible, qui a encore une allocation, passe ce filtre. Il est donc choisi tout de suite, et la branche qui diffère n'est jamais atteinte. La branche d'attente ne vient qu'après. Elle concerne une ressource gratuite épuisée dont la recharge tombe avant la fin du délai. La raison est simple : l'abonnement est déjà payé, la demande part tout de suite sans nouvelle dépense, et l'attente fait courir un risque sur le délai.

Il faut inverser cette priorité quand l'allocation restante de l'abonnement est réservée à des demandes plus importantes, et que la demande courante peut attendre. Il faut aussi que la recharge du gratuit laisse assez de temps pour exécuter la demande et faire le contrôle exigé avant l'échéance. Au réveil, on revérifie la disponibilité : l'heure de recharge ne prouve pas que la capacité est revenue.

Notre portefeuille adapté n'a pas d'abonnement, seulement des routes gratuites et une route payante. Cette priorité ne jouera que si un abonnement éligible est ajouté.

## Limites

- Vingt questions et une seule base : les taux sont propres à ce lot.
- Le cas C11 est rejoué. Les panels où 20B et Cohere votent ensemble sont des hypothèses.
- Sur C11, 20B trouve le bon montant avec une fenêtre fausse, du 2001-01-01 au 2001-12-01. Le résultat n'est juste que parce qu'aucun client n'est né entre le 2000-12-02 et le 2000-12-31. Un verdict correct ne prouve pas que la requête est bonne.
- Qwen n'est pas mesuré sur C16 et C18 à cause des 429.
- Les empreintes de provenance de la partie A ont été calculées sous Windows. Relancé sous Linux, le script donne les mêmes décisions, mais d'autres empreintes, à cause des fins de ligne.

## Contributions

Répartition déduite des commits et des noms de branches, à confirmer par chaque membre.

- Partie A : Maxence Tessier, Aurélien Guillout-Lacomblez.
- Partie B : hechmi Chemli.
- Partie C : Jérémie LEROY-DUBIEF, RASAKARAN Sharusan, Aurelien Roche.
- Ayoub LAMCHICHI : arborescence du dépôt, regroupement des trois parties et assemblage de ce rapport.

La revue croisée est à remplir dans les fichiers review-1.md et review-2.md de chaque partie.

Les scripts et les textes ont été préparés avec l'aide d'assistants d'IA, puis exécutés et vérifiés sur la base. Le rapport de la partie B le signale. La déclaration détaillée du TD 2 reste à ajouter à [td1/ai-assistance.md](../td1/ai-assistance.md), qui ne couvre que le TD 1.

## Suite

Pour le TD 3, il faut chiffrer le contrôle sur les questions où aucun modèle gratuit ne suffit seul. Il s'agit de F2 et F4 pour un chiffre montré au client ou un montant versé, et de C17, où les deux votes s'abstiennent.
