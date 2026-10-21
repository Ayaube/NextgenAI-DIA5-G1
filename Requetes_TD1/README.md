# Requêtes de référence du TD1

Un fichier par question, `C01.sql` à `C20.sql`. Chacun prend un Case :

1. Mets ton nom dans `Auteur`.
2. Écris la requête : un seul `SELECT`, une ligne, une colonne `revenue_cents`.
3. Exécute-la en lecture seule depuis la racine du repo :
   `sqlite3 -readonly data/boutique.sqlite < Requetes_TD1/C01.sql`
4. Note la valeur dans le commentaire `Résultat`.
5. Un autre membre vérifie par une méthode indépendante et remplit `Vérifié par` et `Vérification`.

Ne modifie que ton propre fichier, sur ta branche, puis ouvre une PR vers `main`. Une seule personne reporte ensuite les vingt requêtes et valeurs dans `reference-td1.csv`. La référence ne vient jamais de la réponse d'un LLM, et on ne modifie jamais `data/boutique.sqlite`.
