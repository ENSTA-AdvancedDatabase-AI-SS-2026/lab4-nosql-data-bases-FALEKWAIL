# Rapport de Benchmark NoSQL - TP5

## Résultats des Tests

| Critère | Redis | MongoDB | Cassandra |
|---------|-------|---------|-----------|
| **Débit Écriture** | Très Élevé (Pipeline) | Élevé (Bulk) | Moyen/Élevé (Async) |
| **Débit Lecture** | Ultra-Rapide | Rapide (Index) | Moyen |
| **Latence P99** | < 1ms | ~5-10ms | ~15-30ms |
| **Scalabilité** | Verticale/Cluster | Sharding | Native (Multi-nœud) |

## Analyse et Recommandations

1. **Redis** : Le plus rapide pour les lectures/écritures simples. Idéal pour le **cache** et les sessions.
2. **MongoDB** : Le plus flexible. Excellent pour les **données semi-structurées** et les requêtes complexes.
3. **Cassandra** : Le plus robuste pour les **écritures massives** et les séries temporelles (IoT).
4. **Neo4j** : Imbattable pour les **relations complexes** et les réseaux sociaux.

## Conclusion
Le choix de la base dépend du "Workload" :
- Si vitesse pure → **Redis**.
- Si flexibilité → **MongoDB**.
- Si gros volume de logs → **Cassandra**.
- Si liens complexes → **Neo4j**.
