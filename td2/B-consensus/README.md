# Partie B : comprendre un faux consensus

**Groupe B : Ayoub et Hechmi** — séance du **18 novembre 2026**.

## Travail réalisé

Nous avons cherché si plusieurs modèles donnaient la même valeur fausse sur une même question. Après sélection de la dernière tentative, les 105 lignes de traces donnent 100 cellules : 82 réponses correctes, 14 incorrectes, 2 erreurs SQL et 2 réponses non exécutées.

Aucune valeur fausse n'est partagée par deux modèles sur une même question dans ce lot. L'analyse s'appuie donc sur **DEMO-SQL-C11, un cas historique rejoué**, et sur **DEMO-VOTE, un exemple synthétique**. Ils ne sont pas comptés comme des faux consensus observés dans nos traces.

## Ce que montrent les exemples

Dans le cas C11 rejoué, deux requêtes renvoient 0 au lieu de **446690 centimes** :

- La première ne garde que les clients nés le 1er décembre 2001, au lieu de tous ceux qui ont 25 ans à la date demandée.
- La seconde demande une naissance au plus tard le 1er décembre 2026 et au plus tôt le 1er décembre 2027. Ces conditions sont incompatibles.

La bonne fenêtre va du **1er décembre 2000 exclu au 1er décembre 2001 inclus**. Elle contient 6 clients et 60 lignes de commande. Leur total explique exactement l'écart de 446690 centimes. Un calcul indépendant en Python, à partir des CSV, confirme ce montant.

Le panel fixe « 120B, North, Qwen » garde la bonne valeur dans le scénario reconstitué. Un autre panel contenant les deux modèles fautifs, « 20B, North, 120B », garde 0 avec deux voix sur trois. Le choix du panel compte donc autant que le seuil. Les valeurs des autres modèles utilisées dans cette reconstitution viennent de notre lot : ce n'est pas une mesure complète du pilote historique.

L'exemple synthétique `[0, 0, 100]` illustre le même mécanisme sur une vente inventée de 100 centimes : deux requêtes excluent à tort le premier jour de la période et font gagner 0.

## Fichiers utiles

- [rapport-B.md](rapport-B.md) : recherche dans les traces, explication SQL, panels et limites.
- [traces-td1.csv](traces-td1.csv) : traces analysées.
- [sql](sql/) : requêtes des exemples et requêtes qui isolent l'écart.
- [01_valeurs_fausses_partagees.py](01_valeurs_fausses_partagees.py) : recherche des erreurs communes.
- [03_c11_demo.py](03_c11_demo.py) : exécution des exemples et contrôle indépendant.
- [04_quorum_pairB.py](04_quorum_pairB.py) : comparaison des votes réels et reconstitués.

## Rejouer les vérifications

Depuis la racine du dépôt :

```bash
python td2/B-consensus/01_valeurs_fausses_partagees.py
python td2/B-consensus/03_c11_demo.py
python td2/B-consensus/04_quorum_pairB.py
```

Ces commandes fonctionnent hors ligne. Le deuxième script ouvre `td1/data/boutique.sqlite` en lecture seule et recalcule aussi le montant depuis les CSV de `td1/data`, sans SQL. La table de l'exemple synthétique est créée en mémoire.

## Revues et amélioration proposée

La partie a été relue par le [groupe A — Aurélien et Maxence](review-1.md) et le [groupe C — Jérémie, Aurélien Roche et Sharusan](review-2.md).

La petite amélioration proposée consiste à trier les traces par `date_utc` avant de retenir la dernière tentative. Actuellement, les scripts de recherche et de vote utilisent l'ordre des lignes du CSV. Les résultats sont cohérents sur le fichier actuel, mais ce tri les rendrait moins dépendants du rangement d'un futur export. Cette modification reste à faire.

Un accord entre modèles n'est pas une preuve de justesse. Pour un montant versé, cette analyse justifie un contrôle indépendant, repris dans la [partie C](../C-routing/README.md).

[Retour au TD 2](../README.md)
