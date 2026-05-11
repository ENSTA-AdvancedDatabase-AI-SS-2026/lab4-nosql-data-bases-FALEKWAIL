# Rapport TP2 - MongoDB (Document)

## Ce que j'ai fait
J'ai créé une base de données médicale pour gérer des patients et leurs consultations :
1. **Validation (Schema)** : Utilisation de `$jsonSchema` pour s'assurer que les données (CIN, date de naissance, etc.) sont toujours correctes.
2. **Modélisation** : J'ai mis les consultations directement dans le document du patient (Embedding) car on les lit souvent ensemble. Les analyses sont dans une autre collection (Referencing) car elles peuvent être lourdes.
3. **Agrégation** : J'ai créé des pipelines complexes pour :
   - Compter les maladies par région.
   - Trouver les médicaments les plus prescrits.
   - Calculer le taux de retour des patients chez les médecins.

## Conclusion
MongoDB est très flexible. Le fait de pouvoir mettre des tableaux (consultations) dans les documents évite de faire des "Joins" compliqués comme en SQL.
