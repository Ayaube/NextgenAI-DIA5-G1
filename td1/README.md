# TD 1 : cinq modèles mesurés séparément

Ce dossier contient le kit du cours, la base boutique, nos vingt requêtes de référence et les traces réelles des cinq modèles. Le rapport de la séance est [reports/td1.md](../reports/td1.md).

## Ce qui a été fait

Chaque membre a écrit des requêtes de référence, relues par un autre membre. Les valeurs sont dans reference-td1.csv. Cinq modèles ont été interrogés sur les vingt questions : 105 tentatives et 100 cellules finales. Qwen reste non exécuté sur C16 et C18, après deux erreurs HTTP 429 sur chacune.

- Requetes_TD1 : nos vingt requêtes de référence.
- traces-td1.csv et traces-td1.jsonl : les traces fusionnées des cinq modèles.
- model-question-comparison-en.csv et comparison-pivot.md : le tableau modèles par questions.
- five-model-summary-en.csv : la synthèse par modèle, avec les prix du portefeuille.
- prompts-en.md : le prompt envoyé. ai-assistance.md : l'aide d'IA déclarée.

Pack 2026-10-14-students-1. Empreinte SHA-256 de data/boutique.sqlite : 0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2.

## Rejouer sans clé

Python 3.10 ou plus. Seul check_access.py a besoin du paquet requests et des clés GROQ_API_KEY et OPENROUTER_API_KEY. Le rejeu exécute le SQL enregistré en local, sans appeler de modèle.

```
cd td1
python3 verify-data.py
python3 skeleton-multi-llm-en.py --replay traces-td1.jsonl --state traces-replay.jsonl --out traces-replay.csv
```

La vérification doit finir par "ok": true. Le fichier .gitattributes garde les fins de ligne LF des CSV de données, pour que leurs empreintes restent celles du manifeste. consolider_td1.py reconstruit les tableaux fusionnés à partir des fichiers de chaque opérateur.

Les fichiers atelier-vote.py et atelier-routage.py sont les versions fournies par le kit. Le travail du TD 2 est dans le dossier td2.
