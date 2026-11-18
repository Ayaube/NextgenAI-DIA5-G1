# Partie C : la règle de routage

**Groupe C : Jérémie, Aurélien Roche et Sharusan** — séance du **18 novembre 2026**.

## Travail réalisé

La règle choisit quel modèle appeler selon la famille de questions et quel contrôle demander selon l'usage. Elle s'appuie sur les résultats du TD 1. Les cinq modèles disposent d'une route gratuite dans le cadre étudié ; le choix tient donc aussi compte des quotas, des résultats observés et des possibilités de secours.

| Famille | Questions du TD 1 | Premier modèle | Résultat du modèle sur la famille |
|---|---|---|---|
| F1 — Période | C01, C04, C05, C06, C07, C20 | GPT-OSS 20B | 6/6 |
| F2 — Âge à une date | C02, C08, C09, C11 | GPT-OSS 120B | 4/4 |
| F2b — Âge à la commande | C10 | GPT-OSS 120B | 1/1 |
| F3 — Liste de produits | C03, C12, C13, C14 | GPT-OSS 20B | 4/4 |
| F4 — Combinaisons | C15 à C19 | GPT-OSS 120B | 5/5 |

## Contrôles prévus

- **Tableau interne à faible enjeu :** la règle autorise un modèle seul s'il a tout juste sur la famille dans le TD 1, avec exécution SQL en lecture seule et vérification d'un montant entier en centimes.
- **Chiffre montré au client :** deux membres d'un panel de trois doivent donner le même montant au centime près. Sinon, il faut s'abstenir. Les panels sont précisés dans la règle complète.
- **Montant versé :** comparaison exacte avec une référence SQL indépendante. Une relecture humaine est aussi demandée pour F1, F2 et F2b.

Cohere est exclu du panel sur l'âge à une date, où il obtient 0/4. Les erreurs d'accès de Qwen sur C16 et C18 sont distinguées des réponses fausses.

Si le premier modèle est indisponible, le simulateur cherche une autre route gratuite prévue par la règle. Il peut ensuite attendre une recharge si le délai le permet, utiliser 120B sur une route payante dans la limite du budget, ou s'abstenir. Le contrôle demandé reste nécessaire après le changement de route.

## Résultats du simulateur adapté

| Scénario | Décision |
|---|---|
| `simple` | Appeler 20B sur Groq pour F1 |
| `complex` | Appeler 120B sur Groq pour F4 |
| `deferrable` | Attendre 60 minutes, puis revérifier la disponibilité |
| `urgent` | Utiliser 120B sur OpenRouter dans la limite du budget |
| `budget exhausted` | S'abstenir |
| `high impact` | Appeler 120B et demander une comparaison avec la référence indépendante |
| `unknown capability` | S'abstenir, faute de résultats TD 1 pour cette famille |

Le coût de secours utilisé dans la simulation est de 0,000285 USD par appel, avec l'hypothèse de 1500 jetons en entrée et 100 en sortie, aux prix du portefeuille étudié. Ce n'est pas un coût mesuré lors du TD 2.

Le simulateur choisit une route et indique les contrôles nécessaires. Il ne contacte pas les modèles, n'exécute pas les votes et ne vérifie pas lui-même les montants. Une décision `run` ne signifie donc pas qu'un résultat a déjà été validé.

## Fichiers utiles

- [regle-routage.md](regle-routage.md) : taux par famille, prix du portefeuille et règle détaillée.
- [taux_par_famille.py](taux_par_famille.py) : recalcul des taux à partir du TD 1.
- [atelier-routage.py](atelier-routage.py) : simulateur adapté.
- [simulateur-avant.txt](simulateur-avant.txt) et [simulateur-apres.txt](simulateur-apres.txt) : sorties des sept scénarios avant et après adaptation.
- [Simulateur fourni](../../td1/atelier-routage.py) : version de départ conservée dans `td1`.

## Rejouer les vérifications

Depuis la racine du dépôt, avec Python 3.10 ou plus récent :

```bash
python td2/C-routing/taux_par_famille.py
python td1/atelier-routage.py
python td2/C-routing/atelier-routage.py
python td2/C-routing/atelier-routage.py --scenario deferrable
```

Ces commandes affichent les résultats sans appel réseau. Les taux et les sorties des deux simulateurs ont été vérifiés avec les fichiers conservés.

## Revues et amélioration proposée

La partie a été relue par le [groupe A — Aurélien et Maxence](review-1.md) et le [groupe B — Ayoub et Hechmi](review-2.md).

La branche `customer_figure` existe dans le code, mais aucun des sept scénarios enregistrés ne l'utilise. Ajouter un exemple de chiffre montré au client, puis une variante avec un membre indisponible, permettrait de mieux illustrer le vote 2 sur 3. Ces exemples restent à ajouter.

Les résultats portent sur vingt questions et une seule base. Ils donnent une piste de routage pour notre lot, sans garantir qu'un modèle restera correct sur toutes les futures questions.

[Retour au TD 2](../README.md)
