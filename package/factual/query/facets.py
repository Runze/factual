"""
Factual facets api query
"""

from .read import Read

class Facets(Read):
    def __init__(self, api, path, params={}):
        Read.__init__(self, api, path, params)

    def search(self, terms):
        return self._copy({'q': terms})

    def filters(self, filters):
        return self._copy({'filters': filters})

    def include_count(self, include):
        return self._copy({'include_count': include})

    def min_count(self, min_count):
        return self._copy({'min_count': min_count})

    def geo(self, geo_filter):
        return self._copy({'geo': geo_filter})

    def limit(self, max_rows):
        return self._copy({'limit': max_rows})

    def select(self, fields):
        return self._copy({'select': fields})

    def _copy(self, params):
        return Facets(self.api, self.path, self.merge_params(params))
