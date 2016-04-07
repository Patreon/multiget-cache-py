import importlib


def get_request_cache():
    if _has_flask():
        import flask
        if flask.has_request_context():
            if flask.g.get('request_cache') is None:
                flask.g.request_cache = {}
            return flask.g.request_cache
    return None


def _has_flask():
    return importlib.util.find_spec("flask") is not None
