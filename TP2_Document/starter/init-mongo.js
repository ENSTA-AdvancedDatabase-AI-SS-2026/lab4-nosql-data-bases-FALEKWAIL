// Initialisation de la base médicale
db = db.getSiblingDB('medical_db');

// Créer l'utilisateur
db.createUser({
  user: 'medical_user',
  pwd: 'medical123',
  roles: [{ role: 'readWrite', db: 'medical_db' }]
});

// Créer les tables (collections)
db.createCollection('patients');
db.createCollection('analyses');

print('✅ Base prête !');
