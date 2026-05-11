"""
TP1 - Exercice 4 : Classement des meilleures ventes
Use Case : Top produits ShopFast en temps réel
"""
import redis
from typing import Optional

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

LEADERBOARD_KEY = "leaderboard:sales"


def record_sale(r, product_id, quantity: int = 1):
    # On ajoute des points au produit dans le classement
    r.zincrby(LEADERBOARD_KEY, quantity, str(product_id))


def get_top_products(r, n: int = 10) -> list:
    # On prend les N meilleurs produits avec leurs scores
    results = r.zrevrange(LEADERBOARD_KEY, 0, n - 1, withscores=True)
    return [{"product_id": p[0], "sales": int(p[1])} for p in results]


def get_product_rank(r, product_id) -> Optional[int]:
    # On cherche la place du produit (1er, 2eme, etc.)
    rank = r.zrevrank(LEADERBOARD_KEY, str(product_id))
    return rank + 1 if rank is not None else None


def get_products_between_ranks(r, start_rank: int, end_rank: int) -> list:
    """Récupérer une plage de classement (1-based)"""
    results = r.zrevrange(LEADERBOARD_KEY, start_rank - 1, end_rank - 1, withscores=True)
    return [{"product_id": p[0], "sales": int(p[1])} for p in results]


def simulate_sales_day(r, n_sales: int = 500):
    """
    Simuler une journée de ventes aléatoires
    Générer n_sales ventes aléatoires sur les produits 1-20
    """
    import random
    products = list(range(1, 21))
    for _ in range(n_sales):
        product_id = random.choice(products)
        qty = random.randint(1, 5)
        record_sale(r, product_id, qty)


if __name__ == "__main__":
    r.flushdb()
    
    print("Simulation de ventes...")
    simulate_sales_day(r, 500)
    
    print("\n🏆 Top 5 produits:")
    for i, p in enumerate(get_top_products(r, 5), 1):
        print(f"  {i}. Produit #{p['product_id']} — {int(p['sales'])} ventes")
    
    print(f"\nRang du produit #1: {get_product_rank(r, 1)}")
