

def recDictKeyFetcher(d: dict, *args):
    for arg in args:
        d = d.get(arg, {})
    d = d or None
    return d
