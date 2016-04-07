import inspect
import collections


def get_arg_count(func):
    args, varargs, keywords, defaults = inspect.getargspec(func)
    return len(args)


def convert_args_to_kwargs(func, args):
    args_names, varargs, keywords, defaults = inspect.getargspec(func)
    return dict(zip(args_names, args))


def get_default_args(func):
    """
    returns a dictionary of arg_name:default_values for the input function
    """
    args, varargs, keywords, defaults = inspect.getargspec(func)
    return dict(zip(reversed(args), reversed(defaults)))


def get_object_key(object_, object_key, object_tuple_key):
    """

    :param object_: Object you want to pull a value fron
    :param object_key: String or list/tuple of strings containing field names you want to generate a key from
    :param object_tuple_key: A temporary shortcut until we allow dot.path traversal for object_key.
    Will call getattr(getattr(result, join_table_name), object_key)
    :return:
    """
    if object_tuple_key:
        object_ = getattr(object_, object_tuple_key)
    if isinstance(object_key, (list, tuple)):
        return_string = ''
        for element in object_key:
            return_string += str(getattr(object_, element))
            return_string += '_'
        return return_string
    return str(getattr(object_, object_key))


def get_argument_key(kwargs, argument_key, index):
    """

    :param kwargs: keyword arguments used to kickoff the multiget
    :param argument_key: Name or set of names of keyword arguments to read from
    :param index: which set of arguments are considered
    :return:
    """
    if isinstance(argument_key, (list, tuple)):
        return_string = ''
        for element in argument_key:
            return_string += str(kwargs.get(element)[index] or '')
            if len(argument_key) > 1:
                return_string += '_'
        return return_string
    return str(kwargs.get(argument_key)[index] or '')


def map_objects_to_result(objects, object_key, object_tuple_key, result_value, default_result):
    if not callable(default_result):
        map_ = collections.defaultdict(lambda: default_result)
    else:
        map_ = collections.defaultdict(default_result)

    if not objects:
        return map_

    # This is a hack to get list-type multigets to work
    if default_result is not None and hasattr(map_['iterable'], 'append'):
        for element in objects:
            key = get_object_key(element, object_key, object_tuple_key)
            if not result_value:
                map_[key].append(element)
            elif isinstance(result_value, str):
                map_[key].append(getattr(element, result_value))
            elif isinstance(result_value, (list, tuple)):
                map_[key] = {}
                for attr in result_value:
                    map_[key][attr].append(getattr(element, attr))
    else:
        for element in objects:
            key = get_object_key(element, object_key, object_tuple_key)
            if not result_value:
                map_[key] = element
            elif isinstance(result_value, str):
                map_[key] = getattr(element, result_value)
            elif isinstance(result_value, (list, tuple)):
                map_[key] = {}
                for attr in result_value:
                    map_[key][attr] = getattr(element, attr)

    return map_


def get_request_count(arguments):
    for key, value in arguments.items():
        return len(value)


def map_arguments_to_objects(kwargs, objects, object_key, object_tuple_key, argument_key, result_value, default_result):
    """
    :param kwargs: kwargs used to call the multiget function
    :param objects: objects returned from the inner function
    :param object_key: field or set of fields that map to the kwargs provided
    :param object_tuple_key: A temporary shortcut until we allow dot.path traversal for object_key.
    Will call getattr(getattr(result, join_table_name), object_key)
    :param argument_key: field or set of fields that map to the objects provided
    :param result_value: Limit the fields returned to this field or set of fields (none = whole object)
    :param default_result: If the inner function returned none for a set of parameters, default to this
    :return:
    """

    # Map each object to the set of desired result data using a key
    # that corresponds to the parameters for ordering purposes
    map_ = map_objects_to_result(objects, object_key, object_tuple_key, result_value, default_result)
    element_count = get_request_count(kwargs)
    # Using the map we just made, return the objects in the same order
    # they were primed using the object and argument keys to match against
    return [map_[get_argument_key(kwargs, argument_key, index)] for index in range(0, element_count)]


def get_kwargs_for_function(inner_f):
    args_names, varargs, keywords, defaults = inspect.getargspec(inner_f)
    return args_names
