# A : le vote k sur n

La méthode vote_k_sur_n est complétée dans skeleton-multi-llm-en.py. Une valeur n'est gardée que si elle atteint k voix. Une erreur ou une indisponibilité reste dans n sans voter, et un doublon de modèle est refusé. Sans majorité, la méthode s'abstient.

Sur nos traces, le panel 2 sur 3 et le quorum 3 sur 5 prennent la même décision sur les vingt questions : dix-neuf valeurs justes et une abstention sur C17.

- [rapport-A.md](rapport-A.md) : la méthode, les quatre exemples synthétiques et le tableau des vingt questions.
- [comparaison-quorums.csv](comparaison-quorums.csv) : le même tableau en CSV.
- [tests.txt](tests.txt) : la sortie des tests.

Pour rejouer, depuis la racine du dépôt :

```
python3 td2/A-quorum/test_vote.py
python3 td2/A-quorum/comparaison_quorums.py
```

Le second script régénère le rapport et le CSV. Les copies des traces et de la référence utilisées sont gardées dans ce dossier.
