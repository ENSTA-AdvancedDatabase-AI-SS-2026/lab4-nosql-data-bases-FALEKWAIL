/**
 * TP4 - Exercice 2 : Requêtes de base
 */

// 2.1 : Amis d'Ahmed (E1)
MATCH (ahmed:Etudiant {id: "E1"})-[:CONNAIT]-(ami)
RETURN ami.prenom, ami.nom;

// 2.2 : Suggestions d'amis (amis d'amis mais pas déjà amis)
MATCH (ahmed:Etudiant {id: "E1"})-[:CONNAIT*2]-(suggestion:Etudiant)
WHERE NOT (ahmed)-[:CONNAIT]-(suggestion) AND suggestion <> ahmed
RETURN DISTINCT suggestion.prenom, suggestion.nom, suggestion.universite;

// 2.3 : Étudiants qui suivent le même cours que Fatima (E2) mais ne la connaissent pas
MATCH (fatima:Etudiant {id: "E2"})-[:SUIT]->(c:Cours)<-[:SUIT]-(autre:Etudiant)
WHERE NOT (fatima)-[:CONNAIT]-(autre) AND autre <> fatima
RETURN DISTINCT autre.prenom, autre.nom, c.intitule;

// 2.4 : Clubs les plus populaires
MATCH (e:Etudiant)-[:MEMBRE_DE]->(club:Club)
RETURN club.nom, count(e) AS membres
ORDER BY membres DESC;

// 2.5 : Profil complet d'un étudiant (Ahmed)
MATCH (ahmed:Etudiant {id: "E1"})
OPTIONAL MATCH (ahmed)-[:CONNAIT]-(ami)
OPTIONAL MATCH (ahmed)-[:SUIT]->(cours)
OPTIONAL MATCH (ahmed)-[:MAITRISE]->(comp)
RETURN ahmed.prenom, 
       collect(DISTINCT ami.prenom) AS amis,
       collect(DISTINCT cours.intitule) AS cours,
       collect(DISTINCT comp.nom) AS competences;
