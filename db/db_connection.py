import json
import redis
from api.schema import *


class RedisUnits:

    def __init__(self, host='redis', port=6379):
        """
        Инициализация подключения

        :param host: Хост Redis
        :param port: Порт Redis
        """
        self.connection = redis.Redis(
            host=host,
            port=port
        )

    def get(self, key):
        """
        Получение ShopUnit объекта по id из базы Redis

        :param key: идентификатор объекта ShopUnit
        :return: объект ShopUnit
        """
        val = self.connection.get(key)
        if val:
            return ShopUnit(**json.loads(val))
        return val

    def set(self, key, value: ShopUnit):
        """
        Сохранение объекта ShopUnit в базе Redis

        :param key: ключ сохранения (id объекта)
        :param value: объект, который необходимо записать
        :return: None
        """
        self.connection.set(key, value.json())

    def delete(self, key):
        """
        Удаление объекта по ключу

        :param key: id объекта ShopUnit
        :return: None
        """
        self.connection.delete(key)

    def get_cache(self):
        """
        Получение кэша офферов для статистики

        :return: dict-объект с кэшем офферов
        """

        cache = self.connection.get("date_cache")
        if not cache:
            cache = {'cache': []}
            self.connection.set("date_cache", json.dumps({'cache': []}))
            return cache

        return json.loads(cache)

    def set_cache(self, new_cache):
        """
        Установка нового кэша

        :param new_cache: dict-объект с новым кэшем
        :return: None
        """
        return self.connection.set("date_cache", json.dumps(new_cache))
