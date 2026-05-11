# Rapport TP3 - Cassandra (Column-Family)

## Ce que j'ai fait
J'ai travaillé sur un système IoT pour surveiller le réseau électrique :
1. **Modélisation** : J'ai créé des tables optimisées pour les requêtes (Query-driven design).
   - `mesures_par_capteur` : Partitionnée par `capteur_id` et `date_jour` pour éviter les partitions trop grosses.
2. **Ingestion** : Utilisation de `UNLOGGED BATCH` et des requêtes asynchrones pour insérer 50 000 mesures très rapidement.
3. **Maintenance** : Configuration de la stratégie de compaction `TimeWindowCompactionStrategy` (TWCS) qui est la meilleure pour les données qui ont une date (Time-Series).

## Conclusion
Cassandra est très puissant pour stocker des milliards de lignes. Sa force est de pouvoir écrire très vite sur plusieurs serveurs en même temps, mais il faut bien choisir sa clé de partition au début.
