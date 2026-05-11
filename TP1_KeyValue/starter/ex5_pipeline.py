"""
TP1 - Exercice 5 : Pipeline & Transactions
Use Case : Bulk insert et Passage de commande atomique
"""
import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def bulk_insert_products(r, products_dict: dict):
    # On envoie tout d'un coup pour gagner du temps (Pipeline)
    pipe = r.pipeline()
    for pid, data in products_dict.items():
        pipe.hset(f"product:{pid}", mapping=data)
    pipe.execute()

def process_order_atomic(r, user_id, cart_items: dict):
    # On fait tout d'un bloc (Transaction) : stock + classement
    pipe = r.pipeline()
    try:
        pipe.multi()
        for pid, qty in cart_items.items():
            # Stock et Leaderboard mis à jour ensemble
            pipe.hincrby(f"product:{pid}", "stock", -int(qty))
            pipe.zincrby("leaderboard:sales", int(qty), str(pid))
        
        # Vider le panier
        pipe.delete(f"cart:{user_id}")
        pipe.execute()
        return True
    except Exception:
        pipe.discard()
        return False

if __name__ == "__main__":
    r.flushdb()
    
    # Test Bulk Insert
    products = {
        "10": {"name": "Phone A", "price": "500", "stock": "100"},
        "11": {"name": "Phone B", "price": "600", "stock": "50"},
        "12": {"name": "Phone C", "price": "700", "stock": "30"}
    }
    bulk_insert_products(r, products)
    
    # Test Transaction
    cart = {"10": 2, "11": 1}
    process_order_atomic(r, "user:42", cart)
    
    # Vérifier résultats
    print(f"Stock Phone A: {r.hget('product:10', 'stock')}")
    print(f"Ventes Phone A: {r.zscore('leaderboard:sales', '10')}")
    print(f"Panier user:42 existe encore ? {r.exists('cart:user:42')}")
