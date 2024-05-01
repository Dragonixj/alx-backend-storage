#!/usr/bin/env python3
"""
Task 0: Writing strings to redis
"""
import uuid
from typing import Union

import redis


class Cache:
    """Represents an object for storing in a Redis data storage"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, int, bytes, float]) -> str:
        """Stores a value in a Redis data storage and returns the key"""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)

        return data_key
