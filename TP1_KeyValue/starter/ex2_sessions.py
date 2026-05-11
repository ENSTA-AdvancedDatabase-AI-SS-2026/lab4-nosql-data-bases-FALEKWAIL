"""
TP1 - Exercice 2 : Gestion des sessions utilisateur
Use Case : Sessions avec expiration glissante (sliding expiration)
"""
import redis
import uuid
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

SESSION_TTL = 1800  # 30 minutes en secondes

def create_session(r, user_id):
    # On crée une session qui dure 30 minutes
    session_id = str(uuid.uuid4())
    session_key = f"session:{session_id}"
    r.setex(session_key, SESSION_TTL, user_id)
    return session_id

def get_session(r, session_id):
    # On récupère la session et on remet le compteur à 30 min
    session_key = f"session:{session_id}"
    user_id = r.get(session_key)
    if user_id:
        r.expire(session_key, SESSION_TTL)
    return user_id

def delete_session(r, session_id):
    # On supprime la session
    r.delete(f"session:{session_id}")

if __name__ == "__main__":
    r.flushdb()
    
    print("Création de session...")
    sid = create_session(r, "user:123")
    print(f"Session ID: {sid}")
    
    print(f"User ID récupéré: {get_session(r, sid)}")
    
    ttl = r.ttl(f"session:{sid}")
    print(f"TTL restant: {ttl}s")
    
    print("Suppression...")
    delete_session(r, sid)
    print(f"User ID après suppression: {get_session(r, sid)}")
