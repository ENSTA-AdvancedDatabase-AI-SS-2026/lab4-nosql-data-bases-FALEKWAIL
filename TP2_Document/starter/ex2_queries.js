/**
 * TP2 - Exercice 2 : Requêtes de Base MongoDB
 */
use("medical_db");

// 2.1 : Chercher les diabétiques de plus de 50 ans à Alger
// On utilise regex pour le texte et $lt pour calculer l'âge avec la date
print("\n--- 2.1: Diabétiques > 50 ans à Alger ---");
const diabeticAlger = db.patients.find({
    "antecedents": { $regex: /Diabète/i },
    "adresse.wilaya": "Alger",
    "dateNaissance": { $lt: new Date(new Date().setFullYear(new Date().getFullYear() - 50)) }
}).toArray();
console.table(diabeticAlger.map(p => ({ Nom: p.nom, Prénom: p.prenom, Wilaya: p.adresse.wilaya })));

// 2.2 : Patients avec allergie Pénicilline et au moins 2 consultations
// On utilise $expr et $size pour compter le nombre de consultations dans le tableau
print("\n--- 2.2: Allergie Pénicilline + 2+ consultations ---");
const allergicConsults = db.patients.find({
    "allergies": "Pénicilline",
    $expr: { $gte: [{ $size: "$consultations" }, 2] }
}).toArray();
console.table(allergicConsults.map(p => ({ Nom: p.nom, Allergies: p.allergies, NbConsultations: p.consultations.length })));

// 2.3 : Projection : garder juste Nom, Prénom et la dernière consultation
// $slice -1 permet de prendre juste le dernier élément du tableau
print("\n--- 2.3: Projection Nom, Prénom, Dernière Consultation ---");
const projection = db.patients.find({}, {
    nom: 1,
    prenom: 1,
    derniere_consultation: { $slice: ["$consultations", -1] }
}).limit(5).toArray();
printjson(projection);

// 2.4 Patients sans antécédents dont la tension systolique > 140 en dernière consultation
print("\n--- 2.4: Sans antécédents + Tension > 140 ---");
const highBP = db.patients.find({
    "antecedents": { $size: 0 },
    "consultations": {
        $elemMatch: {
            "tension.systolique": { $gt: 140 }
        }
    }
}).toArray();
printjson(highBP);

// 2.5 : Recherche de texte sur les diagnostics
// Il faut d'abord créer un index de type 'text'
print("\n--- 2.5: Recherche textuelle 'Hypertension' ---");
// Créer l'index text d'abord
db.patients.createIndex({ "consultations.diagnostic": "text" });
const textSearch = db.patients.find({ $text: { $search: "Hypertension" } }).toArray();
print(`Nombre de patients trouvés pour 'Hypertension': ${textSearch.length}`);
