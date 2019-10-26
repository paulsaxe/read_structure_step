REGISTERED_READERS = {}

def register_reader(file_format):

    def decorator_function(fn):

        REGISTERED_READERS[file_format] = fn

        def wrapper_function(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper_function

    return decorator_function


REGISTERED_FORMAT_CHECKERS= {}

def register_format_checker(file_format):

    def decorator_function(fn):

        REGISTERED_FORMAT_CHECKERS[file_format] = fn

        def wrapper_function(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper_function

    return decorator_function
