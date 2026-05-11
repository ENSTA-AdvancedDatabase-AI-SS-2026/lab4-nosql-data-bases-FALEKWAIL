/**
 * TP2 - Exercice 1 : Modélisation MongoDB
 * Use Case : HealthCare DZ - Dossiers Médicaux
 */

// Se connecter à la base médicale
use("medical_db");

// 1.1 : Création de la collection avec validation
// On utilise jsonSchema pour forcer les types de données (nom, age, etc.)
db.createCollection("patients", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cin", "nom", "prenom", "dateNaissance", "sexe", "adresse"],
      properties: {
        cin: { bsonType: "string", description: "CIN obligatoire" },
        nom: { bsonType: "string", description: "Nom obligatoire" },
        prenom: { bsonType: "string", description: "Prénom obligatoire" },
        dateNaissance: { bsonType: "date", description: "Date de naissance obligatoire" },
        sexe: { enum: ["M", "F"], description: "Sexe doit être M ou F" },
        adresse: {
          bsonType: "object",
          required: ["wilaya"],
          properties: {
            wilaya: { bsonType: "string" },
            commune: { bsonType: "string" }
          }
        },
        groupeSanguin: { enum: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"] },
        antecedents: { bsonType: "array", items: { bsonType: "string" } },
        allergies: { bsonType: "array", items: { bsonType: "string" } }
      }
    }
  }
});

// 1.2 : Ajouter 20 patients algériens
const wilayas = ["Alger", "Oran", "Constantine", "Annaba", "Blida", "Tlemcen", "Setif", "Bejaia"];
const pathologies = ["Diabète type 2", "HTA", "Asthme", "Allergie pollen", "Cholestérol"];
const medecins = [
  { nom: "Dr. Mansouri", specialite: "Cardiologie" },
  { nom: "Dr. Belkacem", specialite: "Généraliste" },
  { nom: "Dr. Hamidi", specialite: "Endocrinologie" },
  { nom: "Dr. Saidi", specialite: "Pneumologie" }
];

const patients = [];
for (let i = 1; i <= 20; i++) {
  const age = 20 + (i * 3); // Ages variés
  const dateNaiss = new Date();
  dateNaiss.setFullYear(dateNaiss.getFullYear() - age);

  patients.push({
    _id: new ObjectId(),
    cin: `19${80 + i}123456${i}`,
    nom: ["Bensalem", "Lamine", "Ziri", "Kacimi", "Haddad", "Moussaoui"][i % 6],
    prenom: ["Ahmed", "Fatima", "Mohamed", "Amine", "Siham", "Yasmine"][i % 6],
    dateNaissance: dateNaiss,
    sexe: i % 2 === 0 ? "M" : "F",
    adresse: {
      wilaya: wilayas[i % wilayas.length],
      commune: "Centre Ville"
    },
    groupeSanguin: ["O+", "A+", "B+", "AB-"][i % 4],
    antecedents: i % 3 === 0 ? [pathologies[i % 5], pathologies[(i + 1) % 5]] : [pathologies[i % 5]],
    allergies: i % 4 === 0 ? ["Pénicilline"] : [],
    consultations: [
      {
        id: UUID(),
        date: new Date("2023-05-10"),
        medecin: medecins[i % 4],
        diagnostic: i % 2 === 0 ? "Hypertension" : "Grippe Saisonnière",
        tension: { systolique: 130 + i, diastolique: 80 + (i % 10) },
        medicaments: [{ nom: "Paracétamol", dosage: "1g", duree: "5 jours" }],
        notes: "État stable"
      },
      {
        id: UUID(),
        date: new Date("2024-02-20"),
        medecin: medecins[(i + 1) % 4],
        diagnostic: pathologies[i % 5],
        tension: { systolique: 140, diastolique: 90 },
        medicaments: [{ nom: "Amlodipine", dosage: "5mg", duree: "30 jours" }],
        notes: "Suivi mensuel"
      }
    ]
  });
}

db.patients.insertMany(patients);

// 1.3 : Collection analyses séparée
// On lie les analyses aux patients avec patient_id pour pas que le fichier patient soit trop lourd
const analyses = [];
patients.forEach(p => {
  analyses.push({
    patient_id: p._id,
    date: new Date("2024-03-01"),
    type: "Glycémie",
    resultats: { valeur: 1.1 + (Math.random() * 0.5), unite: "g/L" },
    laboratoire: "Labo Central Alger",
    valide: true
  });
  if (p.antecedents.includes("HTA")) {
    analyses.push({
      patient_id: p._id,
      date: new Date("2024-03-15"),
      type: "ECG",
      resultats: { observation: "Rythme sinusal normal" },
      laboratoire: "Labo El Chiffa",
      valide: true
    });
  }
});

db.analyses.insertMany(analyses);

print("✅ Modélisation terminée.");
print("📊 Patients insérés:", db.patients.countDocuments());
print("📊 Analyses insérées:", db.analyses.countDocuments());
