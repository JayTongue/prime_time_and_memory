# timer_func.py

"""
Utility wrapper functions that measure time, memory, or time and memory.
Imports and uses 'wraps' from 'functools' to preserve dunder methods used in other code portions
"""

from functools import wraps
from time import time
import tracemalloc


def timer_func_wrap(func: callable) -> callable:
    """
    Wrapper function for time which returns a function 
    that subtracts start from end times
    """
    @wraps(func)
    def wrap_time_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        function_time = (t2-t1)
        print(f'Function {func.__name__!r} executed in {function_time}s')
        return result, function_time
    return wrap_time_func()


def measure_memory_usage(func: callable) -> callable:
    """
    measures memory usage with tracemalloc
    delivers the peak memory usage, not total memory usage.
    """
    @wraps(func)
    def wrap_mem_func(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        print('Peak Memory:', (tracemalloc.get_traced_memory()[1])/1000, ' KiB')
        tracemalloc.stop()
        return result
    tracemalloc.clear_traces()
    return wrap_mem_func()


def time_and_memory(func: callable) -> callable:
    """
    Combines the time and memory wrapper functions.
    """
    @wraps(func)
    def wrap_time_mem(*args, **kwargs):
        t1 = time()
        tracemalloc.start()
        result = func(*args, **kwargs)
        t2 = time()
        function_time = (t2-t1)
        function_mem = float((tracemalloc.get_traced_memory()[1])) / 1000
        tracemalloc.stop()
        print(f'Function {func.__name__!r} executed in {function_time}s')
        print(f'Peak Memory: {function_mem} KiB')
        return result, function_time, function_mem
    tracemalloc.clear_traces()
    return wrap_time_mem
