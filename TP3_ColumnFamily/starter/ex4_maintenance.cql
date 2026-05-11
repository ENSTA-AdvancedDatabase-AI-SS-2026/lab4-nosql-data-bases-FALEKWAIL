/**
 * TP3 - Exercice 4 : Maintenance et Compaction (SmartGrid DZ)
 */
USE smartgrid;

-- 4.1 : Configurer TWCS pour les mesures
-- TWCS est idéal pour les séries temporelles car il regroupe les fichiers (SSTables) par temps.
-- Quand les données expirent (TTL), Cassandra peut supprimer des fichiers entiers d'un coup.
ALTER TABLE mesures_par_capteur
WITH compaction = {
  'class': 'TimeWindowCompactionStrategy',
  'compaction_window_unit': 'DAYS',
  'compaction_window_size': 1
};

-- 4.2 : Vérifier les TTL
-- On peut voir quand une ligne va expirer avec la fonction TTL()
SELECT capteur_id, timestamp, TTL(tension_v) 
FROM mesures_par_capteur 
LIMIT 10;

-- 4.3 : Analyse d'une partition "hot"
-- Si un capteur envoie trop de données, sa partition (capteur_id, date) devient trop lourde.
-- Solution : Ajouter une dimension de temps plus fine (ex: bucket par heure) dans la partition key.
-- Exemple : PRIMARY KEY ((capteur_id, date_jour, heure_bucket), timestamp)

print("✅ Configuration de maintenance terminée !");
