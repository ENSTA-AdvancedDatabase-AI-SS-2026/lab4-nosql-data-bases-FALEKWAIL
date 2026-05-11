-- 1.1 : Créer le Keyspace pour le TP
-- On utilise SimpleStrategy car on est en local (RF=1)
CREATE KEYSPACE IF NOT EXISTS smartgrid
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE smartgrid;

-- 1.2 : Table pour stocker les mesures par capteur
-- On regroupe par capteur et par jour pour pas avoir des partitions trop grosses
CREATE TABLE IF NOT EXISTS mesures_par_capteur (
  capteur_id   UUID,
  date_jour    DATE,      -- Partition bucket (un jour)
  timestamp    TIMESTAMP, -- Tri par temps
  wilaya       TEXT,
  commune      TEXT,
  tension_v    FLOAT,
  courant_a    FLOAT,
  puissance_kw FLOAT,
  frequence_hz FLOAT,
  temperature  FLOAT,
  alerte       BOOLEAN,
  code_alerte  TEXT,
  -- Clé de partition composée : (capteur, jour)
  -- Clé de clustering : timestamp pour trier les mesures
  PRIMARY KEY ((capteur_id, date_jour), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 7776000; -- Expire après 90 jours


-- 1.3 : Table pour les alertes par wilaya
-- Pour chercher "les alertes d'Alger aujourd'hui"
CREATE TABLE IF NOT EXISTS alertes_par_wilaya (
  wilaya       TEXT,
  date_jour    DATE,
  timestamp    TIMESTAMP,
  capteur_id   UUID,
  code_alerte  TEXT,
  description  TEXT,
  gravite      INT,
  resolue      BOOLEAN,
  -- On groupe par wilaya et jour
  PRIMARY KEY ((wilaya, date_jour), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 31536000; -- Expire après 1 an


-- 1.4 : Table pour les graphiques (agrégats)
-- Pour voir la conso moyenne par heure
CREATE TABLE IF NOT EXISTS agregats_horaires (
  wilaya            TEXT,
  date_heure        TIMESTAMP,
  nb_capteurs       INT,
  puissance_moy_kw  FLOAT,
  puissance_max_kw  FLOAT,
  puissance_min_kw  FLOAT,
  nb_alertes        INT,
  -- On groupe par wilaya
  PRIMARY KEY (wilaya, date_heure)
) WITH CLUSTERING ORDER BY (date_heure DESC)
  AND default_time_to_live = 157680000; -- Expire après 5 ans


-- Vérification des tables créées
DESCRIBE TABLES;
