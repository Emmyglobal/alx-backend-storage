#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from __future__ import annotations
from functools import wraps
from typing import Union, Callable, Optional
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """ returns a callable """
    datakey = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function """
        self._redis.incr(datakey)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    data = r.get(function_name)
    try:
        data = int(data.decode("utf-8"))
    except Exception:
        data = 0

    print("{} was called {} times:".format(function_name, data))
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache():
    """ A Redis Cache Class """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: str | bytes | int | float) -> str:
        """ Storing method """
        datakey = str(uuid.uuid4())
        self._redis.set(datakey, data)
        return datakey

    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """ control the return value type """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ automatically parametrize Cache.get with the correct
        conversion function."""
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ automatically parametrize Cache.get with the
        correct conversion function. """
        data = self._redis.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0
        return data
