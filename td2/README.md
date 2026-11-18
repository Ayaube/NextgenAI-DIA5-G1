# TD 2 : le quorum, puis la règle de routage

Séance du **18 novembre 2026**, groupe DIA5-G1.

Le but de ce TD est de faire voter plusieurs modèles, de comprendre pourquoi ils peuvent se tromper ensemble, puis de choisir quel modèle appeler selon la question et le niveau de contrôle nécessaire. Le travail utilise les traces du TD 1, sans nouvel appel aux fournisseurs.

## Répartition du travail

| Partie | Groupe | Membres | Travail réalisé |
|---|---|---|---|
| [A — Quorum](A-quorum/README.md) | A | Aurélien et Maxence | Vote k sur n et comparaison des deux quorums sur vingt questions |
| [B — Consensus](B-consensus/README.md) | B | Ayoub et Hechmi | Recherche de valeurs fausses partagées et explication d'un cas rejoué en SQL |
| [C — Routage](C-routing/README.md) | C | Jérémie, Aurélien Roche et Sharusan | Règle par famille de questions et adaptation du simulateur |

Aurélien du groupe A et Aurélien Roche du groupe C sont bien deux personnes différentes.

## Résultats principaux

- **Vote :** le panel 2 sur 3 et le quorum 3 sur 5 donnent chacun 19 consensus corrects et une abstention sur C17. Aucun faux consensus n'est observé dans notre lot.
- **Faux consensus :** aucune valeur fausse n'est partagée par deux modèles sur une même question dans les 100 cellules retenues. La partie B étudie donc le cas C11 rejoué et un exemple synthétique, séparés de nos résultats réels.
- **Routage :** la règle choisit un modèle à partir des résultats du TD 1 et adapte le contrôle à l'usage : tableau interne, chiffre montré au client ou montant versé. Les sorties des sept scénarios sont conservées avant et après adaptation.

Les 8 tests du vote passent. Les vingt décisions et les sorties des simulateurs ont été vérifiées avec le code. Un accord entre modèles ne prouve toutefois pas que leur réponse est juste, et vingt questions ne suffisent pas à garantir les résultats sur d'autres données.

## Revues croisées

Chaque groupe relit les deux parties qu'il n'a pas réalisées. Les six revues sont complétées et datées du 18 novembre 2026.

| Partie relue | Première revue | Deuxième revue |
|---|---|---|
| A | [Groupe B](A-quorum/review-1.md) | [Groupe C](A-quorum/review-2.md) |
| B | [Groupe A](B-consensus/review-1.md) | [Groupe C](B-consensus/review-2.md) |
| C | [Groupe A](C-routing/review-1.md) | [Groupe B](C-routing/review-2.md) |

Les remarques portent sur trois améliorations : mieux distinguer les lettres des modèles et des groupes, trier les tentatives par date dans les scripts de B, et ajouter un scénario de routage pour un chiffre montré au client. Les deux dernières restent des pistes d'amélioration du code et des exemples.

## Lire les résultats et les reproduire

Le [rapport commun](../reports/td2.md) rassemble l'analyse des trois parties. Chaque README de partie donne les liens vers ses fichiers et les commandes pour les rejouer.

Les commandes se lancent **depuis la racine du dépôt**, dans le dossier qui contient `td1` et `td2`, avec Python 3.10 ou plus récent. Elles utilisent uniquement la bibliothèque standard, sans clé API. Si votre installation utilise la commande `python3`, remplacez `python` par `python3`.

La partie A possède ses copies des traces et de la référence. La partie B utilise aussi la base et les CSV de `td1/data`. La partie C lit les traces et les questions du TD 1 et simule les disponibilités : elle ne contacte aucun fournisseur.
