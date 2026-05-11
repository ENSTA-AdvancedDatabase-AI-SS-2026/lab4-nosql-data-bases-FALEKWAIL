# Rapport TP5 - Benchmark & Performance

## Ce que j'ai fait
J'ai comparé les performances des 4 bases de données (Redis, MongoDB, Cassandra, Neo4j) :
1. **Écriture** : Redis est le plus rapide grâce au pipelining. MongoDB et Cassandra sont très performants avec les insertions par lots (Bulk/Batch).
2. **Lecture** : Redis a la latence la plus basse (< 1ms). MongoDB est très rapide pour les recherches par ID grâce aux index.
3. **Charge** : J'ai testé avec 10 clients simultanés pour voir comment la base réagit quand il y a beaucoup de monde.

## Tableau de Décision

| Critère | Redis | MongoDB | Cassandra | Neo4j |
|---------|-------|---------|-----------|-------|
| **Vitesse Écriture** | Ultra-Rapide | Très Rapide | Très Rapide | Moyen |
| **Vitesse Lecture** | < 1ms | ~2-5ms | ~10ms | ~10-20ms |
| **Flexibilité** | Faible | Très Haute | Moyenne | Haute |
| **Use Case** | Cache / Sessions | Web / Apps | IoT / Logs | Réseaux / Bio |

## Conclusion
Il n'y a pas de "meilleure" base, tout dépend du projet. Si on veut de la vitesse pure, on prend Redis. Si on veut stocker des documents, on prend MongoDB. Pour du Big Data, Cassandra est le meilleur.
