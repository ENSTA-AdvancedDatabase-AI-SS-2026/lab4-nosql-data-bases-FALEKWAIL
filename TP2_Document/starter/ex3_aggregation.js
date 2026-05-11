/**
 * TP2 - Exercice 3 : Agrégation
 */
use("medical_db");

// 3.1 : Nombre de diagnostics par wilaya
print("\n--- 3.1: Diagnostics par wilaya ---");
const diagByWilaya = db.patients.aggregate([
    { $unwind: "$consultations" },
    { $group: {
        _id: { wilaya: "$adresse.wilaya", diag: "$consultations.diagnostic" },
        total: { $sum: 1 }
    }},
    { $project: { _id: 0, wilaya: "$_id.wilaya", diagnostic: "$_id.diag", total: 1 }},
    { $sort: { wilaya: 1, total: -1 } }
]).toArray();
printjson(diagByWilaya);

// 3.2 : Médicament le plus donné par spécialité
print("\n--- 3.2: Top médicament par spécialité ---");
const topMed = db.patients.aggregate([
    { $unwind: "$consultations" },
    { $unwind: "$consultations.medicaments" },
    { $group: {
        _id: { spec: "$consultations.medecin.specialite", med: "$consultations.medicaments.nom" },
        count: { $sum: 1 }
    }},
    { $sort: { "_id.spec": 1, count: -1 } },
    { $group: {
        _id: "$_id.spec",
        top_med: { $first: "$_id.med" },
        total: { $first: "$count" }
    }}
]).toArray();
printjson(topMed);

// 3.3 : Consultations par mois
print("\n--- 3.3: Évolution par mois ---");
const monthly = db.patients.aggregate([
    { $unwind: "$consultations" },
    { $group: {
        _id: { 
            annee: { $year: "$consultations.date" },
            mois: { $month: "$consultations.date" }
        },
        nb: { $sum: 1 }
    }},
    { $sort: { "_id.annee": 1, "_id.mois": 1 } }
]).toArray();
printjson(monthly);

// 3.4 : Patients vieux et malades (>60 ans + Diabète + HTA)
print("\n--- 3.4: Moyenne consultations pour patients à risque ---");
const risk = db.patients.aggregate([
    { $match: {
        antecedents: { $all: ["Diabète type 2", "HTA"] },
        dateNaissance: { $lt: new Date(new Date().setFullYear(new Date().getFullYear() - 60)) }
    }},
    { $project: { nb: { $size: "$consultations" } }},
    { $group: { _id: null, moyenne: { $avg: "$nb" } }}
]).toArray();
printjson(risk);

// 3.5 : Top 5 médecins et taux de retour des patients
print("\n--- 3.5: Top 5 médecins et taux de retour ---");
const docs = db.patients.aggregate([
    { $unwind: "$consultations" },
    { $group: {
        _id: { doc: "$consultations.medecin.nom", pat: "$_id" },
        visites: { $sum: 1 }
    }},
    { $group: {
        _id: "$_id.doc",
        total_consults: { $sum: "$visites" },
        pats_uniques: { $sum: 1 },
        retours: { $sum: { $cond: [{ $gt: ["$visites", 1] }, 1, 0] } }
    }},
    { $project: {
        medecin: "$_id",
        taux_retour: { $multiply: [{ $divide: ["$retours", "$pats_uniques"] }, 100] },
        total_consults: 1
    }},
    { $sort: { total_consults: -1 } },
    { $limit: 5 }
]).toArray();
printjson(docs);
