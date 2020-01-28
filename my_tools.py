import time
from functools import wraps
from typing import List


def time_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start_time
        print(f"{func.__name__} took {time_elapsed} seconds")
        return res
    return wrapper


def open_program(filename: str) -> List:
    with open(filename, "r") as f:
        return list(map(int, next(f).split(",")))
