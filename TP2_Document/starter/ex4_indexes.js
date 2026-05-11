/**
 * TP2 - Exercice 4 : Index et Optimisation
 */
use("medical_db");

// 4.1 : Créer des index pour que ça aille plus vite
// Index sur le CIN car c'est unique
db.patients.createIndex({ cin: 1 }, { unique: true });
// Index sur la wilaya pour les stats par région
db.patients.createIndex({ "adresse.wilaya": 1 });
// Index sur la date de naissance pour les filtres par âge
db.patients.createIndex({ dateNaissance: 1 });

// 4.2 : Comparer avec et sans index
print("\n--- 4.2: Test performance avec explain ---");
const stats = db.patients.find({ "adresse.wilaya": "Alger" }).explain("executionStats");
print(`Temps d'exécution: ${stats.executionStats.executionTimeMillis}ms`);
print(`Documents examinés: ${stats.executionStats.totalDocsExamined}`);

// 4.3 : Index composé (plusieurs champs)
// On met wilaya en premier puis le nom
db.patients.createIndex({ "adresse.wilaya": 1, nom: 1 });

// 4.4 : Index TTL pour supprimer automatiquement
// Supprime les analyses après 5 ans (en secondes)
db.analyses.createIndex({ date: 1 }, { expireAfterSeconds: 5 * 365 * 24 * 3600 });

print("\n✅ Index créés avec succès !");
db.patients.getIndexes().forEach(printjson);
