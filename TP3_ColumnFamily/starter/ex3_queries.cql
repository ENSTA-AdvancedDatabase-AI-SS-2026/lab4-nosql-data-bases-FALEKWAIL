/**
 * TP3 - Exercice 3 : Requêtes Monitoring (SmartGrid DZ)
 */
USE smartgrid;

-- 3.1 : Mesures d'un capteur sur les 6 dernières heures
-- On utilise le capteur_id et la date du jour (bucket)
SELECT * FROM mesures_par_capteur
WHERE capteur_id = uuid() -- Remplacer par un vrai ID
  AND date_jour = toDate(now())
  AND timestamp >= toTimestamp(now()) - 6h;

-- 3.2 : Dernière mesure de plusieurs capteurs d'une wilaya
-- LIMIT 1 avec clustering DESC nous donne la plus récente
SELECT * FROM alertes_par_wilaya
WHERE wilaya = 'Alger' AND date_jour = '2024-05-11'
LIMIT 5;

-- 3.3 : Compter les alertes à Alger aujourd'hui
SELECT count(*) FROM alertes_par_wilaya
WHERE wilaya = 'Alger' AND date_jour = toDate(now());

-- 3.4 : Consommation totale par heure
SELECT date_heure, puissance_moy_kw FROM agregats_horaires
WHERE wilaya = 'Alger'
ORDER BY date_heure DESC;

-- 3.5 : Détection d'anomalies (Tension hors 200V-240V)
-- Note: Dans Cassandra, on ne peut pas filtrer sur une colonne non-indexée sans ALLOW FILTERING
-- Sauf si on utilise une table dédiée ou un index.
SELECT * FROM mesures_par_capteur
WHERE tension_v < 200 OR tension_v > 240
ALLOW FILTERING; -- À éviter en prod !

-- 3.7 : Pourquoi éviter ALLOW FILTERING ?
-- Parce que Cassandra doit scanner TOUTE la table, ce qui est très lent.
-- La solution est de créer une table 'alertes_tension' indexée par plage.
