# Revue 1 de la partie C

Relecteurs : groupe A — Aurélien et Maxence
Date : 18 novembre 2026

## Ce qui a été relu et rejoué

Lecture de regle-routage.md, de FAMILY_RULES, de FREE_FALLBACKS et de choose dans atelier-routage.py. Exécution de taux_par_famille.py et des simulateurs avant et après adaptation. Les sorties ont été comparées aux deux fichiers enregistrés.

## Ce qui est juste

Les taux par famille correspondent au tableau. Les sept scénarios avant et après adaptation donnent les sorties attendues. Après adaptation, une demande simple utilise 20B, une combinaison utilise 120B, une demande qui peut attendre est reportée de 60 minutes et une demande urgente peut passer par la route payante. Sans budget pour ce secours, le simulateur s'abstient. Pour un montant versé, il indique bien le contrôle par une référence indépendante.

## Ce qui manque ou doit être corrigé

Il manque un exemple enregistré pour l'usage customer_figure, alors que la branche existe dans choose. Ajouter un scénario « chiffre montré au client » permettrait de voir directement le panel choisi et le seuil de deux voix sur trois. Les sept scénarios actuels couvrent surtout le tableau interne et un cas de versement.
