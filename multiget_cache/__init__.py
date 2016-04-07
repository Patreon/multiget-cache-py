import threading


fallback_cache = None
primary_cache = None


def register_cache(cache):
    """ Either an object conforming to the CacheInterface, or a function which returns one """
    global primary_cache
    primary_cache = cache


def get_cache():
    # TODO(postport): This is too slow and takes too many calls.
    # this is consistent per request, so ensure that this is
    # set once and correct for all contexts.

    cache = _get_primary_cache()
    if cache is not None:
        return cache
    else:
        return _get_fallback_cache()


def clear_cache():
    cache = _get_primary_cache()
    if cache is not None:
        cache.clear()
    _get_fallback_cache().clear()


def _get_fallback_cache():
    global fallback_cache
    if fallback_cache is None:
        fallback_cache = threading.local()
        fallback_cache.cache = {}
    return fallback_cache.cache


def _get_primary_cache():
    global primary_cache
    if callable(primary_cache):
        return primary_cache()
    else:
        return primary_cache
