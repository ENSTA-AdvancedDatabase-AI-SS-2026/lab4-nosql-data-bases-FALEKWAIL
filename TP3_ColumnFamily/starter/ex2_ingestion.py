"""
TP3 - Exercice 2 : Ingestion de données IoT
Use Case : SmartGrid DZ - 10 000 capteurs, 5 minutes de mesures
"""
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, BatchType
import uuid
import random
from datetime import datetime, timedelta
import time

# Configuration
CASSANDRA_HOST = 'localhost'
KEYSPACE = 'smartgrid'
NB_CAPTEURS = 10000
MINUTES_HISTORIQUE = 5

WILAYAS = ["Alger", "Oran", "Constantine", "Annaba", "Blida"]
COMMUNES = {
    "Alger": ["Bab Ezzouar", "Hydra", "El Harrach", "Dar El Beida"],
    "Oran": ["Bir El Djir", "Es Senia", "Arzew"],
    "Constantine": ["El Khroub", "Ain Smara", "Hamma Bouziane"],
    "Annaba": ["El Bouni", "El Hadjar", "Seraidi"],
    "Blida": ["Bougara", "Boufarik", "Larbaa"],
}

def connect():
    """Connexion au cluster Cassandra"""
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect(KEYSPACE)
    return session, cluster


def generate_mesure(capteur_id, wilaya, commune, timestamp):
    """Générer une mesure réaliste pour un capteur"""
    tension_base = 220  # Volts (réseau algérien)
    
    return {
        "capteur_id": capteur_id,
        "date_jour": timestamp.date(),
        "timestamp": timestamp,
        "wilaya": wilaya,
        "commune": commune,
        # Variation normale ± 10V
        "tension_v": round(tension_base + random.gauss(0, 5), 2),
        "courant_a": round(random.uniform(0.5, 15.0), 2),
        "puissance_kw": round(random.uniform(0.1, 3.3), 3),
        "frequence_hz": round(50 + random.gauss(0, 0.1), 2),
        "temperature": round(random.uniform(20, 65), 1),
        # 5% de chance d'alerte
        "alerte": random.random() < 0.05,
    }


def insert_single(session, mesure):
    # On prépare la requête pour gagner en vitesse
    query = """
        INSERT INTO mesures_par_capteur 
        (capteur_id, date_jour, timestamp, wilaya, commune, tension_v, courant_a, puissance_kw, frequence_hz, temperature, alerte)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    prepared = session.prepare(query)
    session.execute(prepared, (
        mesure['capteur_id'], mesure['date_jour'], mesure['timestamp'],
        mesure['wilaya'], mesure['commune'], mesure['tension_v'],
        mesure['courant_a'], mesure['puissance_kw'], mesure['frequence_hz'],
        mesure['temperature'], mesure['alerte']
    ))


def insert_batch(session, prepared_stmt, mesures: list):
    # On utilise un BATCH pour envoyer 50 lignes d'un coup
    batch = BatchStatement(batch_type=BatchType.UNLOGGED)
    for m in mesures:
        batch.add(prepared_stmt, (
            m['capteur_id'], m['date_jour'], m['timestamp'],
            m['wilaya'], m['commune'], m['tension_v'],
            m['courant_a'], m['puissance_kw'], m['frequence_hz'],
            m['temperature'], m['alerte']
        ))
    session.execute(batch)


def run_ingestion(session):
    print(f"Démarrage ingestion : {NB_CAPTEURS} capteurs × {MINUTES_HISTORIQUE} min")
    
    # On prépare la requête UNE SEULE FOIS ici
    query = """
        INSERT INTO mesures_par_capteur 
        (capteur_id, date_jour, timestamp, wilaya, commune, tension_v, courant_a, puissance_kw, frequence_hz, temperature, alerte)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    prepared = session.prepare(query)
    
    start_time = time.time()
    
    # 1. Créer les IDs des capteurs
    capteurs = []
    for _ in range(NB_CAPTEURS):
        wilaya = random.choice(WILAYAS)
        capteurs.append({
            "id": uuid.uuid4(),
            "wilaya": wilaya,
            "commune": random.choice(COMMUNES[wilaya])
        })
    
    # 2. Insérer les données
    total_inserted = 0
    now = datetime.now()
    
    for i in range(MINUTES_HISTORIQUE):
        ts = now - timedelta(minutes=i)
        mesures_batch = []
        
        for c in capteurs:
            m = generate_mesure(c['id'], c['wilaya'], c['commune'], ts)
            mesures_batch.append(m)
            
            # Batch de 50
            if len(mesures_batch) >= 50:
                insert_batch(session, prepared, mesures_batch)
                total_inserted += len(mesures_batch)
                mesures_batch = []
        
        if mesures_batch:
            insert_batch(session, prepared, mesures_batch)
            total_inserted += len(mesures_batch)

    elapsed = time.time() - start_time
    print(f"\n✅ {total_inserted:,} mesures insérées en {elapsed:.1f}s")
    print(f"   Débit : {total_inserted/elapsed:,.0f} mesures/seconde")


if __name__ == "__main__":
    session, cluster = connect()
    run_ingestion(session)
    cluster.shutdown()
