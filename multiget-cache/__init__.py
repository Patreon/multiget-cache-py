import base64
import threading

from .flask_request_cache import get_request_cache, clear_request_cache

fallback_cache = None


def get_cache():
    # TODO(postport): This is too slow and takes too many calls.
    # this is consistent per request, so ensure that this is
    # set once and correct for all contexts.

    # TODO: request_cache isn't priviledged. instead, there's a register_cache function which is used here
    request_cache = get_request_cache()
    if request_cache is not None:
        return request_cache
    else:
        return _get_fallback_cache().cache


def clear_cache():
    clear_request_cache()
    _get_fallback_cache().cache = {}


def _get_fallback_cache():
    if fallback_cache is None:
        fallback_cache = threading.local()
        fallback_cache.cache = {}
    return fallback_cache


def arg_to_key(arg):
    if isinstance(arg, int):
        return str(arg)
    elif isinstance(arg, str):
        return base64.b64encode(bytearray(arg, "utf-8")).decode('utf-8')
    elif isinstance(arg, list):
        return ','.join([arg_to_key(inner_arg) for inner_arg in arg])
    elif arg is None:
        # Unlikely to collide with base64 encoded string above
        return 'value:none'
    else:
        print('trying to get a key for', str(arg))
        raise NotImplemented()
