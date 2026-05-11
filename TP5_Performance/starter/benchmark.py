"""
TP5 - Benchmark Comparatif NoSQL
Mesurer les performances de Redis, MongoDB, Cassandra, Neo4j
"""
import time
import statistics
import json
from typing import Callable, List, Tuple
import redis
from pymongo import MongoClient
from cassandra.cluster import Cluster
from neo4j import GraphDatabase

# ─── Utilitaires de mesure ────────────────────────────────────────────────────

def measure_latency(fn: Callable, iterations: int = 1000) -> dict:
    """
    Exécuter fn iterations fois et retourner les statistiques
    """
    latencies = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        latencies.append((time.perf_counter() - start) * 1000)  # en ms
    
    latencies.sort()
    return {
        "mean_ms": statistics.mean(latencies),
        "p50_ms": latencies[int(0.50 * len(latencies))],
        "p95_ms": latencies[int(0.95 * len(latencies))],
        "p99_ms": latencies[int(0.99 * len(latencies))],
        "max_ms": max(latencies),
        "throughput_rps": 1000 / statistics.mean(latencies)
    }


def print_results(name: str, results: dict):
    print(f"\n{'='*50}")
    print(f" {name}")
    print(f"{'='*50}")
    for k, v in results.items():
        print(f"  {k:20s}: {v:.2f}")


# ─── Ex1 : Benchmark Écriture ─────────────────────────────────────────────────

def benchmark_write_redis(n: int = 100_000):
    # On utilise un pipeline pour envoyer 100 000 clés d'un coup
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    start = time.perf_counter()
    pipe = r.pipeline()
    for i in range(n):
        pipe.set(f"test:{i}", f"valeur_{i}")
        if i % 1000 == 0:
            pipe.execute()
    pipe.execute()
    elapsed = time.perf_counter() - start
    print(f"  Redis: {n/elapsed:.0f} ops/sec")


def benchmark_write_mongodb(n: int = 100_000):
    # On utilise insert_many pour être plus rapide
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    db = client["benchmark"]
    coll = db["test"]
    coll.drop()
    
    docs = [{"_id": i, "val": f"val_{i}"} for i in range(n)]
    start = time.perf_counter()
    # On insère par paquets de 1000
    for i in range(0, n, 1000):
        coll.insert_many(docs[i:i+1000])
        
    elapsed = time.perf_counter() - start
    print(f"  MongoDB: {n/elapsed:.0f} ops/sec")


def benchmark_write_cassandra(n: int = 100_000):
    # On utilise execute_async pour le débit
    cluster = Cluster(['localhost'])
    session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS bench WITH replication = {'class':'SimpleStrategy', 'replication_factor':1}")
    session.set_keyspace("bench")
    session.execute("CREATE TABLE IF NOT EXISTS test (id int PRIMARY KEY, val text)")
    
    prepared = session.prepare("INSERT INTO test (id, val) VALUES (?, ?)")
    start = time.perf_counter()
    
    futures = []
    for i in range(n):
        futures.append(session.execute_async(prepared, (i, f"val_{i}")))
        if len(futures) >= 500:
            for f in futures: f.result()
            futures = []
            
    elapsed = time.perf_counter() - start
    print(f"  Cassandra: {n/elapsed:.0f} ops/sec")
    cluster.shutdown()


# ─── Ex2 : Benchmark Lecture ─────────────────────────────────────────────────

def benchmark_read_redis(n: int = 1000):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # 2.1 Point Lookup
    def point(): r.get(f"test:{random.randint(0, 5000)}")
    print_results("Redis Point Lookup", measure_latency(point, n))
    
    # 2.2 Range Query (Liste des 100 derniers)
    r.lpush("bench_list", *range(1000))
    def range_q(): r.lrange("bench_list", 0, 100)
    print_results("Redis Range (LRANGE 100)", measure_latency(range_q, n))


def benchmark_read_mongodb(n: int = 1000):
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    coll = client["benchmark"]["test"]
    
    # 2.1 Point Lookup
    def point(): coll.find_one({"_id": random.randint(0, 5000)})
    print_results("MongoDB Point Lookup", measure_latency(point, n))
    
    # 2.2 Complex Query (Aggregation)
    def complex_q():
        list(coll.aggregate([
            {"$match": {"_id": {"$gt": 2500}}},
            {"$group": {"_id": None, "avg": {"$avg": "$_id"}}}
        ]))
    print_results("MongoDB Aggregation", measure_latency(complex_q, n // 10))


# ─── Ex3 : Charge concurrente ─────────────────────────────────────────────────
import threading

def benchmark_concurrent(db_name: str, fn: Callable, n_clients: int = 10):
    # On lance plusieurs threads pour simuler des clients
    threads = []
    start = time.perf_counter()
    
    for _ in range(n_clients):
        t = threading.Thread(target=fn)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    elapsed = time.perf_counter() - start
    print(f"  Charge concurrente ({db_name}): {elapsed:.2f}s pour {n_clients} clients")


# ─── Main ─────────────────────────────────────────────────────────────────────
import random

if __name__ == "__main__":
    print("🚀 Benchmark NoSQL - Complet")
    print("="*60)
    
    N = 5000
    
    print(f"\n📝 Ex1 : Benchmark Écriture ({N:,} enregistrements)")
    benchmark_write_redis(N)
    benchmark_write_mongodb(N)
    benchmark_write_cassandra(N)
    
    print(f"\n📖 Ex2 : Benchmark Lecture ({N} requêtes)")
    benchmark_read_redis(1000)
    benchmark_read_mongodb(1000)
    
    print(f"\n⚡ Ex3 : Test Charge Concurrente (10 clients)")
    r = redis.Redis(host='localhost', port=6379)
    benchmark_concurrent("Redis", lambda: r.get("test:1"), 10)
    
    print("\n✅ Benchmark terminé !")
