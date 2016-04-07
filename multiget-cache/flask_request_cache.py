import importlib


def get_request_cache():
    # TODO(postport): This is too slow and takes too many calls.
    # this is consistent per request, so ensure that this is
    # set once and correct for all contexts.

    if _has_flask():
        import flask
        if flask.has_request_context():
            if flask.g.get('request_cache') is None:
                flask.g.request_cache = {}
            return flask.g.request_cache
    return None


def clear_request_cache():
    if _has_flask():
        import flask
        if flask.has_request_context():
            flask.g.request_cache = {}
            return True
    return False


def _has_flask():
    return importlib.util.find_spec("flask") is not None
