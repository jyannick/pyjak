from functools import wraps


def lazy_property(method: callable) -> callable:
    """Decorator that makes a property lazy-evaluated.
    """
    attr_name = '_lazy_' + method.__name__

    @property
    @wraps(method)
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return _lazy_property
