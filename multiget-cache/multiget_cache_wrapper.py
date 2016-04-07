import collections
from .base_cache_wrapper import BaseCacheWrapper
from . import function_tools, get_cache


class MultigetCacheWrapper(BaseCacheWrapper):
    def __init__(self, inner_f, object_key, argument_key, default_result,
                 result_key, object_tuple_key):
        self.argument_tuple_list = []
        self.kwargs_dict = collections.defaultdict(list)
        self.object_key = object_key
        self.result_key = result_key
        self.default_result = default_result
        self.object_tuple_key = object_tuple_key

        # backwards compatibility
        self.multiget = True

        self.argument_key = argument_key
        if not argument_key:
            self.argument_key = function_tools.get_kwargs_for_function(inner_f)
        super(MultigetCacheWrapper, self).__init__(inner_f)

    def __call__(self, *args, **kwargs):
        """
        Pull the return value from the request cache if possible. If not,
        pull the value from calling inner_f, then set the value in request cache
        """
        key = self.mc_key_for(*args, **kwargs)

        # Get the value direct from request cache if it's there.
        cache = get_cache()
        if key in cache:
            return cache[key]
        else:
            self.prime(*args, **kwargs)
            self._issue_gets_for_primes()
            return cache[key]

    def prime(self, *args, **kwargs):
        # Convert positional arguments into kwargs
        kwargs.update(function_tools.convert_args_to_kwargs(self.inner_f, args))
        args = ()

        # Used to calculate cache keys
        self.argument_tuple_list.append((args, kwargs.copy()))

        # Verify argument count (very light measure)
        if len(kwargs) != function_tools.get_arg_count(self.inner_f):
            raise Exception(
                'Invalid multiget args: ' + str(kwargs) + ' for function ' +
                str(self.inner_f)
            )

        # Create parallel lists for each kwarg for each object added to the queue
        for key, value in kwargs.items():
            # sometimes we get a list??
            if hasattr(value, 'append'):
                value = value[0]
            self.kwargs_dict[key].append(str(value))

    def _issue_gets_for_primes(self):
        cache = get_cache()

        # Only call with kwargs because we converted earlier
        objects = self.inner_f(**self.kwargs_dict)
        # For the objects that were returned, reorder them such that they match
        # the order they were primed in, and if nothing was returned for a set
        # of arguments, use the provided default value
        mapped_objects = function_tools.map_arguments_to_objects(
            self.kwargs_dict, objects, self.object_key, self.object_tuple_key,
            self.argument_key, self.result_key, self.default_result
        )
        for (args, kwargs), mapped_object in zip(self.argument_tuple_list, mapped_objects):
            key = self.mc_key_for(*args, **kwargs)
            cache[key] = mapped_object

        # Reset
        self.argument_tuple_list = []
        self.kwargs_dict = collections.defaultdict(list)


def multiget_cached(object_key, argument_key=None, default_result=None,
                    result_fields=None, join_table_name=None):
    """
    :param object_key: the names of the attributes on the result object that are meant to match the function parameters
    :param argument_key: the function parameter names you wish to match with the `object_key`s.
    By default, this will be all of your wrapped function's arguments, in order.
    So, you'd really only use this when you want to ignore a given function argument.
    :param default_result: The result to put into the cache if nothing is matched.
    :param result_fields: The attribute on your result object you wish to return the value of.
    By default, the whole object is returned.
    :param join_table_name: A temporary shortcut until we allow dot.path traversal for object_key.
    Will call getattr(getattr(result, join_table_name), object_key)
    :return: A wrapper that allows you to queue many O(1) calls and flush the queue all at once,
    rather than executing the inner function body N times.
    """

    def create_wrapper(inner_f):
        return MultigetCacheWrapper(
            inner_f, object_key, argument_key, default_result, result_fields,
            join_table_name
        )

    return create_wrapper
