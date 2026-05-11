"""
TP1 - Exercice 1 : Structures de données Redis
Use Case : ShopFast - Gestion des produits, paniers et navigation
"""
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def store_product(r, product_id, product_data: dict):
    # On stocke les infos du produit (dictionnaire) dans Redis
    r.hset(f"product:{product_id}", mapping=product_data)


def get_product(r, product_id):
    # On récupère toutes les infos du produit
    data = r.hgetall(f"product:{product_id}")
    return data if data else None


def add_to_cart(r, user_id, product_id, quantity: int = 1):
    # On ajoute la quantité d'un produit dans le panier
    r.hincrby(f"cart:{user_id}", str(product_id), quantity)


def get_cart(r, user_id):
    # On récupère tout le contenu du panier
    return r.hgetall(f"cart:{user_id}")


def record_view(r, user_id, product_id, max_history: int = 10):
    # On met le produit au début de la liste et on limite la taille
    key = f"history:{user_id}"
    r.lpush(key, str(product_id))
    r.ltrim(key, 0, max_history - 1)


def get_history(r, user_id):
    # Récupérer l'historique complet
    return r.lrange(f"history:{user_id}", 0, -1)


def add_product_to_category(r, category, product_id):
    # On ajoute le produit dans l'ensemble de la catégorie
    r.sadd(f"category:{category}", str(product_id))


def get_products_in_categories(r, *categories):
    # On cherche les produits qui sont dans toutes les catégories données
    keys = [f"category:{c}" for c in categories]
    return r.sinter(*keys)


if __name__ == "__main__":
    # Test manuel
    r.flushdb()
    
    # Stocker des produits
    store_product(r, 1, {"name": "Samsung A54", "price": "65000", "category": "phones", "stock": "15"})
    store_product(r, 2, {"name": "Laptop HP", "price": "120000", "category": "laptops", "stock": "8"})
    
    # Tester le panier
    add_to_cart(r, "user:42", 1, 2)
    print("Panier:", get_cart(r, "user:42"))
    
    # Tester l'historique
    for pid in [1, 2, 1, 3]:
        record_view(r, "user:42", pid)
    print("Historique:", get_history(r, "user:42"))
