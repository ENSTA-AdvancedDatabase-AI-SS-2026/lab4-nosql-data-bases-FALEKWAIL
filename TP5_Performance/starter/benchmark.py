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
    def point_lookup():
        r.get(f"test:{random.randint(0, 10000)}")
    
    res = measure_latency(point_lookup, n)
    print_results("Redis Read (Point Lookup)", res)


def benchmark_read_mongodb(n: int = 1000):
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    coll = client["benchmark"]["test"]
    def point_lookup():
        coll.find_one({"_id": random.randint(0, 10000)})
        
    res = measure_latency(point_lookup, n)
    print_results("MongoDB Read (Point Lookup)", res)


# ─── Main ─────────────────────────────────────────────────────────────────────
import random

if __name__ == "__main__":
    print("🚀 Benchmark NoSQL - Comparatif")
    print("="*60)
    
    N = 5000  # On réduit pour que ça aille vite pendant le TP
    
    print(f"\n📝 Benchmark Écriture ({N:,} enregistrements)")
    benchmark_write_redis(N)
    benchmark_write_mongodb(N)
    benchmark_write_cassandra(N)
    
    print(f"\n📖 Benchmark Lecture ({N} requêtes)")
    benchmark_read_redis(1000)
    benchmark_read_mongodb(1000)
    
    print("\n✅ Benchmark terminé !")
