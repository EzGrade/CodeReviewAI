"""
Redis client
"""

import aioredis

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
        self.client: aioredis.Redis = aioredis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    async def set(self, key, value, ex=None) -> bool:
        """
        Set key-value pair in Redis
        :param key:
        :param value:
        :param ex:
        :return:
        """
        return await self.client.set(key, value, ex=ex)

    async def get(self, key) -> str:
        """
        Get value by key
        :param key:
        :return:
        """
        return await self.client.get(key)

    async def delete(self, key) -> int:
        """
        Delete key
        :param key:
        :return:
        """
        return await self.client.delete(key)

    async def exists(self, key) -> bool:
        """
        Check if key exists
        :param key:
        :return:
        """
        return await self.client.exists(key)

    async def flushdb(self):
        """
        Flush database
        :return:
        """
        return await self.client.flushdb()
