# Partie A : le vote k sur n

**Groupe A : Aurélien et Maxence** — séance du **18 novembre 2026**.

## Travail réalisé

La méthode `vote_k_sur_n` est complétée dans [skeleton-multi-llm-en.py](skeleton-multi-llm-en.py). Elle garde une valeur seulement si elle atteint le seuil k, qui doit être une majorité stricte du nombre total de membres n.

Une erreur ou une indisponibilité reste comptée dans n sans voter. Un doublon du même fournisseur et du même modèle est refusé. La valeur 0 est un vote valable. Si aucune valeur n'atteint le seuil, la méthode s'abstient. La référence sert à vérifier la réponse après le vote, jamais à la choisir.

## Résultats

| Vote | Modèles | Consensus corrects | Faux consensus | Abstentions |
|---|---|---:|---:|---:|
| 2 sur 3 | GPT-OSS 120B, North, Qwen | 19 | 0 | 1 |
| 3 sur 5 | Les trois précédents, GPT-OSS 20B et Dots | 19 | 0 | 1 |

Les deux votes s'abstiennent sur **C17**. La bonne valeur, 258180 centimes, n'a qu'une voix dans le panel de trois et deux voix dans celui de cinq. Elle n'atteint donc aucun des deux seuils.

Les 8 tests passent, notamment sur les seuils, les doublons, les erreurs et la valeur 0. Les quatre exemples synthétiques montrent un accord, un désaccord, des indisponibilités et un faux consensus. Ces exemples sont séparés des mesures sur les vingt questions.

Dans le rapport, les lettres **A à E désignent les modèles**, pas nos groupes de travail : A = 120B, B = 20B, C = North, D = Qwen et E = Dots. Le panel « A+C+D » correspond donc à « 120B, North, Qwen ».

## Fichiers utiles

- [rapport-A.md](rapport-A.md) : méthode, résultats détaillés et explication des différences de voix.
- [comparaison-quorums.csv](comparaison-quorums.csv) : tableau des vingt décisions.
- [test_vote.py](test_vote.py) et [tests.txt](tests.txt) : tests et sortie enregistrée.
- [vote-synthetic.jsonl](vote-synthetic.jsonl) : résultats des quatre exemples synthétiques.
- [traces-td1-merged.csv](traces-td1-merged.csv), [reference-td1.csv](reference-td1.csv) et [provenance.json](provenance.json) : données utilisées et origine des tentatives retenues.

## Rejouer les vérifications

Depuis la racine du dépôt, avec Python 3.10 ou plus récent :

```bash
python td2/A-quorum/test_vote.py
python td2/A-quorum/atelier-vote.py
python td2/A-quorum/comparaison_quorums.py
```

Tout fonctionne hors ligne. La dernière commande régénère le rapport, le CSV comparatif, les traces fusionnées, la provenance et les résultats synthétiques. Elle réécrit donc ces fichiers.

## Revues et limites

La partie a été relue par le [groupe B — Ayoub et Hechmi](review-1.md) et le [groupe C — Jérémie, Aurélien Roche et Sharusan](review-2.md). La remarque principale concerne la distinction entre les lettres des modèles et celles des groupes, précisée ci-dessus.

Ces résultats concernent uniquement notre lot. Ajouter des modèles ne garantit pas une meilleure réponse : 120B et 20B appartiennent à la même famille et peuvent partager des erreurs. La [partie B](../B-consensus/README.md) explique ce risque.

[Retour au TD 2](../README.md)
