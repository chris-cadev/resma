import inspect
from functools import wraps

# if more flexibility is needed consult: https://chatgpt.com/s/t_6862fb0be9a88191b47c8ceeee0956b7
def cacheable(key=None, cache_interactor='cache'):
    def decorator(method):
        sig = inspect.signature(method)

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            bound = sig.bind(self, *args, **kwargs)
            bound.apply_defaults()

            cache = getattr(self, cache_interactor, None)
            if not cache:
                return method(self, *args, **kwargs)

            if not key:
                raise ValueError("param_name must be provided for cache key extraction")

            if key not in bound.arguments:
                raise ValueError(f"Parameter '{key}' not found in method arguments")

            cache_key = bound.arguments[key]
            cached = cache.get(key=cache_key)
            if cached:
                return cached

            result = method(self, *args, **kwargs)
            if result != None:
                cache.set(key=cache_key, value=result)
            return result

        return wrapper
    return decorator
