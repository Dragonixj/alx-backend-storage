#!/usr/bin/env python3
"""
Writing strings to redis 
"""

import uuid
from functools import wraps
from typing import Any, Callable, Optional, Union

import redis


def count_calls(method: Callable) -> Callable:
    """Increment values"""

    @wraps(method)
    def wrappper(self, *args, **kwargs) -> Any:
        """retruns the given method after incrementging its call counter"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrappper


class Cache:
    """Represents an object for storing in a Redis data storage"""

    def __init__(self) -> None:
        """init a private redis instance and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in a Redis data storage and returns the key"""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)

        return data_key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """Retrive stored data"""
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        return self.get(key, str)

    def get_int(self, key: int) -> int:
        "Retrive stored integer"
        return self.get(key, int)
