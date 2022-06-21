import json
import redis
from schema import *


class RedisUnits:

    def __init__(self, host='localhost', port=6379):
        self.connection = redis.Redis(
            host=host,
            port=port
        )

    def get(self, key):
        val = self.connection.get(key)
        if val:
            return ShopUnit(**json.loads(val))
        return val

    def set(self, key, value: ShopUnit):
        self.connection.set(key, value.json())

    def delete(self, key):
        self.connection.delete(key)

