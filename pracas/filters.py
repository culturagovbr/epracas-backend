from rest_framework import filters


class UnaccentSearchFilter(filters.SearchFilter):
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
        '~': 'unaccent__icontains'
    }
