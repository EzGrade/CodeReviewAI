"""
Redis client
"""

import redis

import config


class RedisClient:
    """
    Redis client that provides methods to interact with Redis
    """

    def __init__(
            self,
            host: str = config.REDIS_HOST,
            port: int = config.REDIS_PORT,
            db: str = config.REDIS_DB,
            password: str = config.REDIS_PASSWORD
    ):
        self.host: str = host
        self.port: int = port
        self.db: str = db
        self.password: str = password
        self.client: redis.Redis = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    def set(self, key, value, ex=None) -> bool:
        """
        Set key-value pair in Redis
        :param key:
        :param value:
        :param ex:
        :return:
        """
        return self.client.set(key, value, ex=ex)

    def get(self, key) -> str:
        """
        Get value by key
        :param key:
        :return:
        """
        return self.client.get(key)

    def delete(self, key) -> int:
        """
        Delete key
        :param key:
        :return:
        """
        return self.client.delete(key)

    def exists(self, key) -> bool:
        """
        Check if key exists
        :param key:
        :return:
        """
        return self.client.exists(key)

    def flushdb(self):
        """
        Flush database
        :return:
        """
        return self.client.flushdb()
