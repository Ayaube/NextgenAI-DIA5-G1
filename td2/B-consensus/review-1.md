# Revue 1 de la partie B

Relecteurs : groupe A — Aurélien et Maxence
Date : 18 novembre 2026

## Ce qui a été relu et rejoué

Lecture de rapport-B.md et des requêtes SQL. Exécution de 01_valeurs_fausses_partagees.py, 03_c11_demo.py et 04_quorum_pairB.py, puis comparaison avec les résultats de la partie A.

## Ce qui est juste

La recherche retrouve 100 cellules et aucune valeur fausse partagée sur une même question dans notre lot. Les exemples sont bien séparés des mesures réelles. Sur le cas C11 rejoué, les deux mauvaises requêtes renvoient 0, alors que la référence et le calcul indépendant en Python donnent 446690 centimes. Les 6 clients et les 60 lignes de commande expliquent bien tout l'écart. Les résultats des quorums sur nos traces concordent avec la partie A.

## Ce qui manque ou doit être corrigé

Petite amélioration dans 01_valeurs_fausses_partagees.py et 04_quorum_pairB.py : la dernière tentative est choisie selon l'ordre des lignes du CSV. Il serait plus solide de trier les lignes par date_utc avant de garder la dernière, comme dans la partie A. Les résultats vérifiés sont cohérents sur le fichier actuel, mais un export rangé autrement pourrait changer la sélection.
