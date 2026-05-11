// TP4 - Exercice 1 : Création du graphe UniConnect DZ
// Effacer la base pour partir propre
MATCH (n) DETACH DELETE n;

// ─── 1.1 : Contraintes d'unicité ─────────────────────────────────────────────
CREATE CONSTRAINT etudiant_id IF NOT EXISTS FOR (e:Etudiant) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT cours_code IF NOT EXISTS FOR (c:Cours) REQUIRE c.code IS UNIQUE;
CREATE CONSTRAINT competence_nom IF NOT EXISTS FOR (c:Competence) REQUIRE c.nom IS UNIQUE;

// ─── 1.2 : Créer les compétences ──────────────────────────────────────────────
UNWIND [
  {nom: "Python", categorie: "Programmation"},
  {nom: "Java", categorie: "Programmation"},
  {nom: "SQL", categorie: "Bases de Données"},
  {nom: "NoSQL", categorie: "Bases de Données"},
  {nom: "Machine Learning", categorie: "IA"},
  {nom: "Deep Learning", categorie: "IA"},
  {nom: "React", categorie: "Web"},
  {nom: "Docker", categorie: "DevOps"},
  {nom: "Linux", categorie: "Systèmes"},
  {nom: "Réseaux", categorie: "Infrastructure"}
] AS comp
MERGE (:Competence {nom: comp.nom, categorie: comp.categorie});

// ─── 1.3 : Créer les cours ────────────────────────────────────────────────────
UNWIND [
  {code: "INFO401", intitule: "Bases de Données Avancées", credits: 6, dept: "Informatique"},
  {code: "INFO402", intitule: "Intelligence Artificielle", credits: 6, dept: "Informatique"},
  {code: "INFO403", intitule: "Développement Web", credits: 4, dept: "Informatique"},
  {code: "INFO404", intitule: "Systèmes Distribués", credits: 5, dept: "Informatique"},
  {code: "INFO405", intitule: "Cloud Computing", credits: 4, dept: "Informatique"}
] AS cours
MERGE (:Cours {code: cours.code, intitule: cours.intitule, 
               credits: cours.credits, departement: cours.dept});

// 1.4 : Créer 50 étudiants algériens (liste simplifiée pour le TP)
UNWIND range(1, 50) AS i
WITH i, 
     ["Ahmed", "Fatima", "Yacine", "Amel", "Karim", "Sonia", "Mohamed", "Meriem", "Ryad", "Leila"][(i-1)%10] AS prenom,
     ["Bensalem", "Ouali", "Hamidi", "Zitouni", "Mansouri", "Belkacem", "Saidi", "Kacimi"][(i-1)%8] AS nom,
     ["USTHB", "UMBB", "USTO", "UMC", "UBMA"][(i-1)%5] AS univ,
     ["Informatique", "Mathématiques", "GL", "Telecoms"][(i-1)%4] AS filiere,
     ["Alger", "Boumerdes", "Oran", "Constantine", "Annaba"][(i-1)%5] AS ville
MERGE (e:Etudiant {id: "E" + i})
SET e.prenom = prenom, e.nom = nom, e.universite = univ, e.filiere = filiere, e.annee = (i % 5) + 1, e.ville = ville;

// 1.5 : Créer des relations sociales (CONNAIT)
// On lie chaque étudiant à son voisin pour que tout soit connecté
MATCH (e1:Etudiant), (e2:Etudiant)
WHERE e1.id = "E" + toInteger(substring(e2.id, 1)) + 1
MERGE (e1)-[:CONNAIT {depuis: 2023}]-(e2);

// On ajoute quelques amis dans la même université
MATCH (e1:Etudiant), (e2:Etudiant)
WHERE e1.universite = e2.universite AND e1.id < e2.id AND rand() < 0.2
MERGE (e1)-[:CONNAIT {depuis: 2024}]-(e2);

// 1.6 : Relations académiques (SUIT)
// Chaque étudiant suit 2 cours au hasard
MATCH (e:Etudiant), (c:Cours)
WITH e, c, rand() AS r ORDER BY r
WITH e, collect(c)[0..2] AS cours_list
UNWIND cours_list AS c
MERGE (e)-[:SUIT {note: round(rand() * 20, 1)}]->(c);

// 1.7 : Compétences (MAITRISE)
MATCH (e:Etudiant), (comp:Competence)
WITH e, comp, rand() AS r ORDER BY r
WITH e, collect(comp)[0..3] AS comp_list
UNWIND comp_list AS comp
MERGE (e)-[:MAITRISE {niveau: ["Débutant", "Intermédiaire", "Avancé"][toInteger(rand()*3)]}]->(comp);

// 1.8 : Entreprises et Clubs
MERGE (ent:Entreprise {nom: "Sonatrach", secteur: "Energie", ville: "Alger"});
MERGE (club:Club {nom: "Club IA", universite: "USTHB", domaine: "IA"});

// Quelques stages et membres
MATCH (e:Etudiant) WHERE rand() < 0.1
MATCH (ent:Entreprise {nom: "Sonatrach"})
MERGE (e)-[:A_STAGE_CHEZ {annee: 2024}]->(ent);

MATCH (e:Etudiant {universite: "USTHB"}) WHERE rand() < 0.3
MATCH (club:Club {nom: "Club IA"})
MERGE (e)-[:MEMBRE_DE {role: "Membre"}]->(club);

// Vérification
MATCH (n) RETURN labels(n)[0] AS type, count(n) AS total ORDER BY total DESC;
MATCH ()-[r]->() RETURN type(r) AS relation, count(r) AS total ORDER BY total DESC;
