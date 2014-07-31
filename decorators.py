from functools import wraps


def one_to_one(regex, admin_only=False):
    def wrap(f):
        passed_args = []

        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        wrapped_f.meta = getattr(f, "meta", {})

        wrapped_f.meta["regex"] = regex
        wrapped_f.meta["only_to_direct_mentions"] = False
        wrapped_f.meta["only_to_admin"] = admin_only
        wrapped_f.meta["private_only"] = True
        wrapped_f.meta["__doc__"] = f.__doc__
        return wrapped_f
    return wrap

def respond_to(regex, admin_only=False):
    def wrap(f):
        passed_args = []

        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        wrapped_f.meta = getattr(f, "meta", {})

        wrapped_f.meta["regex"] = regex
        wrapped_f.meta["only_to_direct_mentions"] = True
        wrapped_f.meta["only_to_admin"] = admin_only
        wrapped_f.meta["private_only"] = False
        wrapped_f.meta["__doc__"] = f.__doc__
        return wrapped_f
    return wrap

def hear(regex, admin_only=False):
    def wrap(f):
        passed_args = []

        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        wrapped_f.meta = getattr(f, "meta", {})

        wrapped_f.meta["regex"] = regex
        wrapped_f.meta["only_to_direct_mentions"] = False
        wrapped_f.meta["only_to_admin"] = admin_only
        wrapped_f.meta["private_only"] = False
        wrapped_f.meta["__doc__"] = f.__doc__
        return wrapped_f
    return wrap