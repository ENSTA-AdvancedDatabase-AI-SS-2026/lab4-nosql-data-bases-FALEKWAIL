# Rapport TP4 - Neo4j (Graph)

## Ce que j'ai fait
J'ai modélisé un réseau social universitaire :
1. **Graphe** : Création de nœuds (Etudiants, Cours, Clubs) et de relations (CONNAIT, SUIT, MEMBRE_DE).
2. **Algorithmes** :
   - `shortestPath` : Pour trouver comment deux étudiants peuvent se rencontrer.
   - `Louvain` : Pour détecter les cercles d'amis (communautés).
   - `Similarité de Jaccard` : Pour recommander des amis qui ont les mêmes cours et compétences.
3. **Recommandations** : Création d'un score basé sur les amis en commun et les intérêts partagés.

## Conclusion
Neo4j est parfait pour les réseaux sociaux. Faire ces requêtes en SQL prendrait des dizaines de lignes et serait très lent, alors qu'en Cypher c'est simple et rapide.
