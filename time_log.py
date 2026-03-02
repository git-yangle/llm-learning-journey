import functools
import time

def time_logger(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f"DEBUG: {func.__name__} 耗时 {end - start:.2f}s")
        return result
    return wrapper

# 然后在你的 mock_llm_call 上方加上 @time_logger