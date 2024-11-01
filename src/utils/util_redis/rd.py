import redis

import config


class RedisClient:
    def __init__(
            self,
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            password=config.REDIS_PASSWORD
    ):
        self.host = host
        self.port = port
        self.db = db
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    def set(
            self,
            key,
            value,
            ex=None
    ) -> bool:
        return self.client.set(key, value)

    def get(
            self,
            key
    ) -> str:
        return self.client.get(key)

    def delete(
            self,
            key
    ) -> int:
        return self.client.delete(key)

    def exists(
            self,
            key
    ) -> bool:
        return self.client.exists(key)

    def flushdb(self):
        return self.client.flushdb()
