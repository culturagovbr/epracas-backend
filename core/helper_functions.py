from functools import partial

from rest_framework.reverse import reverse


def _(view, *args, **kwargs):
    return partial(reverse, view, *args, **kwargs)
