# Revue 1 de la partie A

Relecteurs : groupe B — Ayoub et Hechmi
Date : 18 novembre 2026

## Ce qui a été relu et rejoué

Lecture de vote_k_sur_n, de rapport-A.md et du tableau comparaison-quorums.csv. Les 8 tests de test_vote.py et les quatre exemples de atelier-vote.py ont été rejoués. Les vingt décisions ont aussi été recalculées avec les fonctions de comparaison_quorums.py et comparées au CSV.

## Ce qui est juste

Le vote respecte la majorité stricte, refuse les doublons et garde les modèles indisponibles dans le nombre total de membres. La valeur 0 est bien acceptée. Sans assez de voix, le vote s'abstient sans utiliser la référence pour choisir une réponse. Les résultats correspondent au rapport : 19 consensus corrects et une abstention sur C17, pour les deux quorums.

## Ce qui manque ou doit être corrigé

Petite remarque de présentation : les lettres A à E désignent les modèles dans le rapport, alors que A, B et C désignent aussi nos groupes. Ajouter une phrase qui distingue ces deux usages éviterait les confusions lors de la lecture du panel « A+C+D ». Le calcul lui-même est correct.
