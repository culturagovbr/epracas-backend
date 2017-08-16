from functools import partial

from rest_framework.reverse import reverse


def test_reverse(view, *args, **kwargs):
    return partial(reverse, view, *args, **kwargs)
