# TD2 — Pair A : vote et comparaison des quorums

Consigne finale `2026-11-18-students-5`, 18 novembre 2026. Contribution **Pair A / étape 1 uniquement**, à intégrer au rapport collectif après la revue croisée.

## 1. Méthode `vote_k_sur_n`

Implémentation dans [skeleton-multi-llm-en.py](../skeleton-multi-llm-en.py), méthode `Orchestrateur.vote_k_sur_n`. Le reste du squelette TD1 est conservé.

`n` compte tous les membres, y compris les erreurs et indisponibilités. Le code refuse un seuil non entier ou hors de `n // 2 < k <= n`, ainsi qu'un doublon `(provider, model_requested)`. Il compte les valeurs entières des propositions `executed` uniquement. Dès qu'une valeur atteint k voix, il renvoie cette valeur et les modèles qui la soutiennent. Sinon il s'abstient, conserve le plus grand nombre de voix observé et renvoie `value=None`, `models=[]`. La valeur 0 est un vote valide.

La référence n'entre jamais dans le vote : `correct` et `incorrect` deviennent tous deux `executed`. Les erreurs (`sql_invalid`, `not_executed`, etc.) deviennent `error` et ne votent pas, même si une valeur résiduelle était présente. Comparaison à la référence seulement après les deux décisions. Une trace absente fait échouer le script : elle n'est pas inventée ni assimilée à une panne du fournisseur.

## 2. Quatre exemples synthétiques exécutés

Commande : `python atelier-vote.py`. Sortie brute : [vote-synthetic.jsonl](../vote-synthetic.jsonl). Ces exemples ne sont pas des résultats réels sur la boutique.

| Exemple | Propositions | Décision | Valeur | Voix | Référence | Accord |
|---|---|---|---:|---:|---:|---|
| agreement | 100, 100, 120 | consensus | 100 | 2 | 100 | oui |
| disagreement | 100, 110, 120 | abstention | — | 1 | 100 | sans réponse |
| unavailable | 100, indisponible, indisponible | abstention | — | 1 | 100 | sans réponse |
| wrong consensus | 0, 0, 100 | consensus | 0 | 2 | 100 | non |

Le cas « wrong consensus » montre pourquoi l'accord n'est pas une preuve de justesse. L'analyse SQL détaillée relève de Pair B.

## 3. Données et sélection des tentatives

- A : Groq / `openai/gpt-oss-120b`, [trace_A.csv](../trace_A.csv).
- B : Groq / `openai/gpt-oss-20b`, [traces-B.csv](../traces-B.csv).
- C : OpenRouter / `cohere/north-mini-code:free`, [traces-C.csv](../traces-C.csv).
- D : Groq / `qwen/qwen3.8-27b`, [traces-D.csv](../traces-D.csv).
- E : OpenRouter / `dots-studio/dots-3-note-preview:free`, [copie locale traces-E.csv](../traces-E.csv), récupérée dans [le commit GitHub source](https://github.com/Ayaube/NextgenAI-DIA5-G1/blob/af26f14022229f3bbfc2c095e9976b426c9fc0d9/traces-E.csv).

105 lignes originales, dont 25 pour D, réduites à **100 cellules : 5 modèles × 20 questions** en gardant la dernière tentative par fournisseur/modèle/question. Tri chronologique stable : à date identique, l'ordre du CSV départage les tentatives. Aucun retour à une ancienne tentative réussie après un échec. Les exports A/B/C/D de GitHub sont identiques aux fichiers locaux ; les 20 références numériques et les hashes de prompts concordent pour les cinq modèles.

Le panel 2/3 est **A+C+D** ; le quorum 3/5 est **A+B+C+D+E**. B et A partagent la famille GPT-OSS : cinq modèles ne signifient pas cinq sources d'erreur indépendantes. Aucun nouvel appel API, aucune modification des prompts, aucune réouverture du TD1.

Référence : [reference-td1.csv](../reference-td1.csv). [Traces fusionnées](../traces-td1-merged.csv). [Provenance des 100 cellules](../provenance.json) : fichier, numéro d'enregistrement CSV (hors en-tête, pas numéro de ligne physique), date, valeur, verdict, statut HTTP et erreur.

## 4. Comparaison commentée des vingt questions

Montants en centimes HT. « Voix » est le maximum obtenu par une valeur, même en cas d'abstention. « Accord » ne note que les consensus ; une abstention n'est pas une réponse numérique fausse.

| Cas | Référence | 2/3 : décision / valeur | Voix | Accord | 3/5 : décision / valeur | Voix | Accord |
|---|---:|---|---:|---|---|---:|---|
| C01 | 792800 | consensus / 792800 | 3/3 | oui | consensus / 792800 | 5/5 | oui |
| C02 | 590320 | consensus / 590320 | 2/3 | oui | consensus / 590320 | 3/5 | oui |
| C03 | 936350 | consensus / 936350 | 3/3 | oui | consensus / 936350 | 5/5 | oui |
| C04 | 2826250 | consensus / 2826250 | 3/3 | oui | consensus / 2826250 | 5/5 | oui |
| C05 | 38480 | consensus / 38480 | 3/3 | oui | consensus / 38480 | 5/5 | oui |
| C06 | 0 | consensus / 0 | 3/3 | oui | consensus / 0 | 5/5 | oui |
| C07 | 13970 | consensus / 13970 | 3/3 | oui | consensus / 13970 | 5/5 | oui |
| C08 | 605580 | consensus / 605580 | 2/3 | oui | consensus / 605580 | 4/5 | oui |
| C09 | 487980 | consensus / 487980 | 2/3 | oui | consensus / 487980 | 3/5 | oui |
| C10 | 558980 | consensus / 558980 | 2/3 | oui | consensus / 558980 | 4/5 | oui |
| C11 | 446690 | consensus / 446690 | 2/3 | oui | consensus / 446690 | 4/5 | oui |
| C12 | 1666490 | consensus / 1666490 | 3/3 | oui | consensus / 1666490 | 5/5 | oui |
| C13 | 107740 | consensus / 107740 | 3/3 | oui | consensus / 107740 | 5/5 | oui |
| C14 | 0 | consensus / 0 | 3/3 | oui | consensus / 0 | 5/5 | oui |
| C15 | 168680 | consensus / 168680 | 2/3 | oui | consensus / 168680 | 3/5 | oui |
| C16 | 376740 | consensus / 376740 | 2/3 | oui | consensus / 376740 | 3/5 | oui |
| C17 | 258180 | abstention / — | 1/3 | sans réponse | abstention / — | 2/5 | sans réponse |
| C18 | 62480 | consensus / 62480 | 2/3 | oui | consensus / 62480 | 3/5 | oui |
| C19 | 1990 | consensus / 1990 | 2/3 | oui | consensus / 1990 | 3/5 | oui |
| C20 | 1106090 | consensus / 1106090 | 3/3 | oui | consensus / 1106090 | 5/5 | oui |

**Bilan :** 2/3 = 19 consensus corrects, 0 faux consensus, 1 abstention(s). 3/5 = 19 consensus corrects, 0 faux consensus, 1 abstention(s). Changements de décision/valeur : aucun.

### Explication de toutes les différences de voix et de marge

La marge vaut **nombre maximum de voix − k** : négative, aucun consensus ; nulle, seuil atteint exactement. L'ajout de B et E peut augmenter les voix sans améliorer cette marge puisque le seuil passe aussi de 2 à 3. Les valeurs et verdicts des deux modèles ajoutés sont cités pour chaque question ci-dessous ; ceux du panel initial figurent dans la section suivante.

| Cas | Effet de l'ajout de B et E (valeurs en centimes, verdicts des traces) |
|---|---|
| C01 | Même décision ; B=792800 (correct) ; E=792800 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C02 | Même décision ; B=0 (incorrect) ; E=590320 (correct). Max voix 2→3, seuil 2→3, marge +0→+0. |
| C03 | Même décision ; B=936350 (correct) ; E=936350 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C04 | Même décision ; B=2826250 (correct) ; E=2826250 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C05 | Même décision ; B=38480 (correct) ; E=38480 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C06 | Même décision ; B=0 (correct) ; E=0 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C07 | Même décision ; B=13970 (correct) ; E=13970 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C08 | Même décision ; B=605580 (correct) ; E=605580 (correct). Max voix 2→4, seuil 2→3, marge +0→+1. |
| C09 | Même décision ; B=487980 (correct) ; E=134660 (incorrect). Max voix 2→3, seuil 2→3, marge +0→+0. |
| C10 | Même décision ; B=558980 (correct) ; E=558980 (correct). Max voix 2→4, seuil 2→3, marge +0→+1. |
| C11 | Même décision ; B=446690 (correct) ; E=446690 (correct). Max voix 2→4, seuil 2→3, marge +0→+1. |
| C12 | Même décision ; B=1666490 (correct) ; E=1666490 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C13 | Même décision ; B=107740 (correct) ; E=107740 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C14 | Même décision ; B=0 (correct) ; E=0 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |
| C15 | Même décision ; B=168680 (correct) ; E=138920 (incorrect). Max voix 2→3, seuil 2→3, marge +0→+0. |
| C16 | Même décision ; B=376740 (correct) ; E=211260 (incorrect). Max voix 2→3, seuil 2→3, marge +0→+0. |
| C17 | Même décision ; B=258180 (correct) ; E=152730 (incorrect). Max voix 1→2, seuil 2→3, marge -1→-1. |
| C18 | Même décision ; B=62480 (correct) ; E=39580 (incorrect). Max voix 2→3, seuil 2→3, marge +0→+0. |
| C19 | Même décision ; B=1990 (correct) ; E=— (sql_invalid). Max voix 2→3, seuil 2→3, marge +0→+0. |
| C20 | Même décision ; B=1106090 (correct) ; E=1106090 (correct). Max voix 3→5, seuil 2→3, marge +1→+2. |

**C02 :** A et D votent 590 320 ; C est `sql_invalid`. Le 2/3 atteint exactement son seuil. B vote 0 (`incorrect`) tandis que E vote 590 320 (`correct`) : le 3/5 atteint aussi exactement son seuil, avec trois voix. L'erreur SQL de C ne réduit ni n=3 ni n=5.

**C17 :** A=258 180 (`correct`), C=105 840 (`incorrect`), D=248 490 (`incorrect`) : une voix maximum, donc abstention 2/3. B ajoute 258 180 (`correct`), E ajoute 152 730 (`incorrect`) : deux voix maximum, insuffisantes pour k=3. La référence vaut 258 180 mais le vote n'a pas le droit de la choisir grâce à cette connaissance.

**C16 et C18 :** la dernière tentative D est `not_executed` et ne vote pas. A et C suffisent au 2/3 ; B les rejoint au 3/5, tandis que E propose une autre valeur incorrecte. **C19 :** E est `sql_invalid` et D propose 83 580 (`incorrect`) ; A, B et C soutiennent 1 990, d'où le consensus 3/5. Ces verdicts proviennent des traces ; aucune panne HTTP 429 n'est supposée sans trace correspondante.

### Valeurs et verdicts exacts des 100 cellules retenues

| Cas | A : GPT-OSS-120B | B : GPT-OSS-20B | C : North | D : Qwen | E : Dots |
|---|---|---|---|---|---|
| C01 | 792800 (correct) | 792800 (correct) | 792800 (correct) | 792800 (correct) | 792800 (correct) |
| C02 | 590320 (correct) | 0 (incorrect) | — (sql_invalid) | 590320 (correct) | 590320 (correct) |
| C03 | 936350 (correct) | 936350 (correct) | 936350 (correct) | 936350 (correct) | 936350 (correct) |
| C04 | 2826250 (correct) | 2826250 (correct) | 2826250 (correct) | 2826250 (correct) | 2826250 (correct) |
| C05 | 38480 (correct) | 38480 (correct) | 38480 (correct) | 38480 (correct) | 38480 (correct) |
| C06 | 0 (correct) | 0 (correct) | 0 (correct) | 0 (correct) | 0 (correct) |
| C07 | 13970 (correct) | 13970 (correct) | 13970 (correct) | 13970 (correct) | 13970 (correct) |
| C08 | 605580 (correct) | 605580 (correct) | 0 (incorrect) | 605580 (correct) | 605580 (correct) |
| C09 | 487980 (correct) | 487980 (correct) | 0 (incorrect) | 487980 (correct) | 134660 (incorrect) |
| C10 | 558980 (correct) | 558980 (correct) | 548920 (incorrect) | 558980 (correct) | 558980 (correct) |
| C11 | 446690 (correct) | 446690 (correct) | 0 (incorrect) | 446690 (correct) | 446690 (correct) |
| C12 | 1666490 (correct) | 1666490 (correct) | 1666490 (correct) | 1666490 (correct) | 1666490 (correct) |
| C13 | 107740 (correct) | 107740 (correct) | 107740 (correct) | 107740 (correct) | 107740 (correct) |
| C14 | 0 (correct) | 0 (correct) | 0 (correct) | 0 (correct) | 0 (correct) |
| C15 | 168680 (correct) | 168680 (correct) | 168680 (correct) | 0 (incorrect) | 138920 (incorrect) |
| C16 | 376740 (correct) | 376740 (correct) | 376740 (correct) | — (not_executed) ; HTTP 429 | 211260 (incorrect) |
| C17 | 258180 (correct) | 258180 (correct) | 105840 (incorrect) | 248490 (incorrect) | 152730 (incorrect) |
| C18 | 62480 (correct) | 62480 (correct) | 62480 (correct) | — (not_executed) ; HTTP 429 | 39580 (incorrect) |
| C19 | 1990 (correct) | 1990 (correct) | 1990 (correct) | 83580 (incorrect) | — (sql_invalid) |
| C20 | 1106090 (correct) | 1106090 (correct) | 1106090 (correct) | 1106090 (correct) | 1106090 (correct) |

## 5. Reproduction, tests et contribution

Depuis td2/A-quorum, avec Python standard, sans clé API :

```powershell
..\..\.venv\Scripts\python.exe atelier-vote.py
..\..\.venv\Scripts\python.exe comparaison_quorums.py
..\..\.venv\Scripts\python.exe test_vote.py
..\..\.venv\Scripts\python.exe atelier-vote.py --traces traces-td1-merged.csv --case C02
```

Le script produit ce rapport, le [CSV comparatif](../comparaison-quorums.csv), les traces fusionnées, leur provenance et les quatre exemples. Les tests vérifient notamment les seuils, doublons, indisponibilités, zéros, votes incorrects et les 2/3 et 3/5 sur toutes les combinaisons de quatre valeurs possibles. Sortie : [tests.txt](../tests.txt).

Contribution préparée avec assistance de Codex : implémentation, exécution hors ligne, comparaison et explications. Membres de Pair A : **à compléter**. À relire et expliquer à Pair B/C lors de la revue croisée. Le rapport collectif intégrera leurs travaux séparément ; ils ne sont pas réalisés dans cette contribution. Aucun commit, push ou dépôt Moodle effectué.
