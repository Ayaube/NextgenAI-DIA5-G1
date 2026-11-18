# B : le faux consensus

Dans nos cent cellules du TD 1, deux modèles ne se trompent jamais avec la même valeur sur une même question. On a donc analysé le cas historique C11 prévu par le sujet.

Sur C11, deux requêtes différentes renvoient 0 alors que la référence vaut 446690 centimes. La première ne garde que les clients nés le 2001-12-01. La seconde demande une date de naissance à la fois avant 2026-12-01 et après 2027-12-01, ce qui est impossible. La bonne fenêtre va du 2000-12-01 exclu au 2001-12-01 inclus. Six clients y sont, et leurs commandes font exactement 446690 centimes.

- [rapport-B.md](rapport-B.md) : la recherche, l'analyse SQL, la requête qui isole l'écart et les votes.
- [sql](sql) : toutes les requêtes utilisées.

Pour rejouer, depuis la racine du dépôt :

```
python3 td2/B-consensus/01_valeurs_fausses_partagees.py
python3 td2/B-consensus/03_c11_demo.py
python3 td2/B-consensus/04_quorum_pairB.py
```

Le deuxième script ouvre td1/data/boutique.sqlite en lecture seule et refait aussi le calcul en Python, sans SQL.
