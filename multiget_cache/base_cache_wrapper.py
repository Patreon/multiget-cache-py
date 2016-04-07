import base64

from . import get_cache, function_tools


class BaseCacheWrapper(object):
    # TODO: Implement kwargs as well.
    def __init__(self, inner_f):
        self.inner_f = inner_f
        self.f_prefix = inner_f.__module__ + '.' + inner_f.__name__

    def __call__(self, *args, **kwargs):
        """Pull the return value from the request cache if possible. If not,
        pull the return value from memcache if possible. If not, pull the
        value from calling inner_f, then set the value in request cache
        and memcache where needed."""
        key = self.mc_key_for(*args, **kwargs)

        # Get the value direct from request cache if it's there.
        cache = get_cache()
        if key in cache:
            return cache[key]
        else:
            key = self.mc_key_for(*args, **kwargs)
            result = self.inner_f(*args, **kwargs)
            cache[key] = result
            return result

    def mc_key_for(self, *args, **kwargs):
        # Convert args to kwargs
        kwargs.update(function_tools.convert_args_to_kwargs(self.inner_f, args))
        args = ()

        return ':'.join(
            [self.f_prefix] +
            [self.arg_to_key(arg) for arg in args] +
            [self.arg_to_key(key + str(arg)) for key, arg in sorted(kwargs.items())]
        )

    @staticmethod
    def arg_to_key(arg):
        if isinstance(arg, int):
            return str(arg)
        elif isinstance(arg, str):
            return base64.b64encode(bytearray(arg, "utf-8")).decode('utf-8')
        elif isinstance(arg, list):
            return ','.join([BaseCacheWrapper.arg_to_key(inner_arg) for inner_arg in arg])
        elif arg is None:
            # Unlikely to collide with base64 encoded string above
            return 'value:none'
        else:
            print('trying to get a key for', str(arg))
            raise NotImplemented()

    def delete(self, *args):
        """Remove the key from the request cache and from memcache."""
        cache = get_cache()
        key = self.mc_key_for(*args)
        if key in cache:
            del cache[key]


def cached():
    def create_wrapper(inner_f):
        return BaseCacheWrapper(inner_f)

    return create_wrapper
