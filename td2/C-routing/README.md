# C : la règle de routage

Pour chaque famille de questions, la règle choisit le modèle le moins cher qui a tout juste au TD 1, puis un niveau de contrôle selon ce que coûte une erreur. Le niveau dépend de l'usage : tableau interne, chiffre montré au client ou montant versé.

En résumé, un modèle seul suffit pour un tableau interne quand il a fait 100 % sur la famille. Un chiffre montré au client demande un vote 2 sur 3. Un montant versé demande une comparaison avec une requête de référence indépendante. Cohere ne vote jamais sur l'âge à une date, où il fait 0 sur 4.

- [regle-routage.md](regle-routage.md) : les taux exacts du TD 1 par famille, les prix, la règle complète et l'analyse de choose.
- [atelier-routage.py](atelier-routage.py) : le simulateur adapté à notre règle. La version fournie est restée dans td1.
- [simulateur-avant.txt](simulateur-avant.txt) et [simulateur-apres.txt](simulateur-apres.txt) : les sept scénarios avant et après adaptation.

Pour rejouer, depuis la racine du dépôt :

```
python3 td2/C-routing/taux_par_famille.py
python3 td1/atelier-routage.py
python3 td2/C-routing/atelier-routage.py
```
