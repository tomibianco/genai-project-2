import redis
import os



# Endpoint de Redis ElastiCache Serverless
REDIS_HOST = "redis-xxxx.cache.amazonaws.com"  # Reemplazar con el endpoint real
REDIS_PORT = 6379

# Conexión a Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)
