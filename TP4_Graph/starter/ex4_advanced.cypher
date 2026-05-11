/**
 * TP4 - Exercice 4 : Requêtes Avancées
 */

// 4.1 : Trouver un tuteur
// "Étudiant en Master (année > 3) qui maîtrise Python (Avancé) et a eu >14 en BDD"
MATCH (tuteur:Etudiant)-[:MAITRISE {niveau: "Avancé"}]->(:Competence {nom: "Python"})
MATCH (tuteur)-[s:SUIT]->(c:Cours {intitule: "Bases de Données Avancées"})
WHERE tuteur.annee >= 3 AND s.note > 14
RETURN tuteur.prenom, tuteur.nom, s.note AS note_bdd;

// 4.2 : Réseau alumni dans une entreprise (Sonatrach)
// "Qui de mon réseau (jusqu'à 3 sauts) travaille chez Sonatrach ?"
MATCH (moi:Etudiant {id: "E1"})-[:CONNAIT*1..3]-(alumni:Etudiant)-[:A_STAGE_CHEZ]->(e:Entreprise {nom: "Sonatrach"})
RETURN DISTINCT alumni.prenom, alumni.nom, alumni.universite;

// 4.3 : Détection de similarité (Jaccard)
// "Étudiants les plus similaires à Ahmed (E1) basés sur les cours et compétences"
MATCH (moi:Etudiant {id: "E1"})-[:SUIT|MAITRISE]->(item)
WITH moi, count(item) AS mes_items, collect(id(item)) AS mes_ids
MATCH (autre:Etudiant)-[:SUIT|MAITRISE]->(item)
WHERE autre <> moi
WITH moi, mes_items, mes_ids, autre, count(item) AS ses_items, collect(id(item)) AS ses_ids
WITH moi, autre, mes_items, ses_items,
     size([x IN mes_ids WHERE x IN ses_ids]) AS intersection
WITH moi, autre,
     toFloat(intersection) / (mes_items + ses_items - intersection) AS jaccard_index
RETURN autre.prenom, autre.nom, jaccard_index
ORDER BY jaccard_index DESC
LIMIT 5;

// 4.4 : Analyse de l'influence (Bonus : Centralité propre)
// Qui sont les étudiants qui sont des "ponts" entre universités ?
MATCH (e1:Etudiant)-[:CONNAIT]-(e2:Etudiant)
WHERE e1.universite <> e2.universite
RETURN e1.prenom, count(e2) AS connexions_externes
ORDER BY connexions_externes DESC
LIMIT 5;
