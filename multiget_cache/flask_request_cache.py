import importlib


def get_request_cache():
    try:
        import flask
        if flask.has_request_context():
            if flask.g.get('request_cache') is None:
                flask.g.request_cache = {}
            return flask.g.request_cache
    except ImportError:
        pass
    return None
