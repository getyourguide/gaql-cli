"""Output GoogleAdsRows in different formats"""
import collections


def flatten(d, parent_key=''):
    """recursively flatten a nested dictionary of reasonable depth"""
    items = []
    for k, v in d.items():
        key = parent_key + '.' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, key).items())
        else:
            items.append((key, v))
    return dict(items)
