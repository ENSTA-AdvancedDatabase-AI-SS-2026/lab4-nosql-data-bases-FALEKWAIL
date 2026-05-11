# Rapport TP1 - Redis (Key-Value)

## Ce que j'ai fait
Dans ce TP, j'ai utilisé Redis pour gérer les données d'un site e-commerce :
1. **Produits (Hash)** : Stockage des infos produits. C'est très rapide pour lire un objet complet.
2. **Panier (Hash)** : Utilisation de `HINCRBY` pour gérer les quantités simplement.
3. **Historique (List)** : Utilisation de `LPUSH` et `LTRIM` pour garder seulement les 10 derniers articles vus.
4. **Catégories (Set)** : Utilisation de `SINTER` pour trouver les produits qui appartiennent à plusieurs catégories en même temps.

## Conclusion
Redis est parfait pour les données qui changent souvent (paniers, sessions) car il stocke tout en mémoire, ce qui le rend extrêmement rapide.
