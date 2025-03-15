import json
import os
import redis


class MemoryManager:
    def __init__(self, host="localhost", port=6379):
        self.host = host or os.environ.get("REDIS_HOST")
        self.port = port or int(os.environ.get("REDIS_PORT"))
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)
        self.redis = redis.Redis(connection_pool=self.pool)

    def store_message(self, sender, message, response):
        """Almacena la conversación en Redis"""
        key = f"chat_history:{sender}"
        chat_history = self.get_history(sender)
        chat_history.append({"user": message, "bot": response})
        
        # Guarda la conversación en formato JSON
        self.redis.set(key, json.dumps(chat_history), ex=86400)  # Tiempo de expiración en segundos (24 horas)

    def get_history(self, sender):
        """Obtiene el historial de conversación"""
        key = f"chat_history:{sender}"
        history_json = self.redis.get(key)
        return json.loads(history_json) if history_json else []

    def clear_history(self, sender):
        """Elimina la memoria de un usuario"""
        key = f"chat_history:{sender}"
        self.redis.delete(key)