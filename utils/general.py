

def recDictKeyFetcher(d: dict, *args):
    """Feches the mentioned keys in args, recursively in the given dictionary d"""
    for arg in args:
        d = d.get(arg, {})
    d = d or None
    return d
