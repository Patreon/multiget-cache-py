from . import get_cache, function_tools, arg_to_key


class BaseCache(object):
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
            # TODO: kill bracket access, use .set and enforce the availability of that interface
            cache[key] = result
            return result

    def mc_key_for(self, *args, **kwargs):
        # Convert args to kwargs
        kwargs.update(function_tools.convert_args_to_kwargs(self.inner_f, args))
        args = ()

        return ':'.join(
            [self.f_prefix] +
            [arg_to_key(arg) for arg in args] +
            [arg_to_key(key + str(arg)) for key, arg in sorted(kwargs.items())]
        )

    def delete(self, *args):
        """Remove the key from the request cache and from memcache."""
        cache = get_cache()
        key = self.mc_key_for(*args)
        if key in cache:
            # TODO: kill bracket access, use .delete and enforce the availability of that interface
            del cache[key]


def cached():
    def create_wrapper(inner_f):
        return BaseCache(inner_f)

    return create_wrapper
