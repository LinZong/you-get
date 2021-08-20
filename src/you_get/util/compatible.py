import sys

def print_more_compatible(*args, **kwargs):
    import builtins as __builtin__
    """Overload default print function as py (<3.3) does not support 'flush' keyword.
    Although the function name can be same as print to get itself overloaded automatically,
    I'd rather leave it with a different name and only overload it when importing to make less confusion.
    """
    # nothing happens on py3.3 and later
    if sys.version_info[:2] >= (3, 3):
        return __builtin__.print(*args, **kwargs)

    # in lower pyver (e.g. 3.2.x), remove 'flush' keyword and flush it as requested
    doFlush = kwargs.pop('flush', False)
    ret = __builtin__.print(*args, **kwargs)
    if doFlush:
        kwargs.get('file', sys.stdout).flush()
    return ret
