from abc import ABCMeta, abstractmethod


class CacheInterface(object):
    """
    A subset of dict's interface, as BaseCacheWrapper expects to receive from its calls to `get_cache()`
    """
    _metaclass__ = ABCMeta

    @abstractmethod
    def get(self, k, d=None):
        """ D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None. """
        pass

    @abstractmethod
    def __getitem__(self, y):
        """ x.__getitem__(y) <==> x[y] """
        pass

    @abstractmethod
    def items(self):
        """ D.items() -> a set-like object providing a view on D's items """
        pass

    @abstractmethod
    def __setitem__(self, *args, **kwargs):
        """ Set self[key] to value. """
        pass

    @abstractmethod
    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        pass

    @abstractmethod
    def __delitem__(self, *args, **kwargs):  # real signature unknown
        """ Delete self[key]. """
        pass

    @abstractmethod
    def __contains__(self, *args, **kwargs):
        """ True if D has a key k, else False. """
        pass
