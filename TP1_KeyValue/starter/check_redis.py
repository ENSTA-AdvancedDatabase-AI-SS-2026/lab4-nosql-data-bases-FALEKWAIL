import redis
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    print(f"Redis Ping: {r.ping()}")
except Exception as e:
    print(f"Error connecting to Redis: {e}")
