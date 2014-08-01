"""
Factual table api query
"""

from .base import Base
from .read import Read

DEFAULT_LIMIT = 20

class Table(Read):
    def __init__(self, api, path, params={}, factual_id=None):
        self.cached_schema = None
        self.fact_id = factual_id
        Read.__init__(self, api, path, params)

    def factual_id(self, factual_id):
        return self._copy({}, factual_id)

    def search(self, terms):
        return self._copy({'q': terms})

    def filters(self, filters):
        return self._copy({'filters': filters})

    def include_count(self, include):
        return self._copy({'include_count': include})

    def geo(self, geo_filter):
        return self._copy({'geo': geo_filter})

    def limit(self, max_rows):
        return self._copy({'limit': max_rows})

    def select(self, fields):
        return self._copy({'select': fields})

    def sort(self, sort_params):
        return self._copy({'sort': sort_params})

    def offset(self, offset):
        return self._copy({'offset': offset})

    def page(self, page_num, limit=DEFAULT_LIMIT):
        limit = DEFAULT_LIMIT if limit < 1 else limit
        page_num = 1 if page_num < 1 else page_num
        return self.offset((page_num - 1) * limit).limit(limit)

    def sort_asc(self, *args):
        return self.sort(','.join(field + ':asc' for field in args))

    def sort_desc(self, *args):
        return self.sort(','.join(field + ':desc' for field in args))

    def threshold(self, threshold):
        return self._copy({'threshold': threshold})

    def schema(self):
        if not self.cached_schema:
            self.cached_schema = self.api.schema(self)
        return self.cached_schema

    @Base.path.getter
    def path(self):
        path = self._path
        if self.fact_id:
            path += '/' + self.fact_id
        return path

    def _copy(self, params, factual_id=None):
        return Table(self.api, self._path, self.merge_params(params), factual_id or self.fact_id)
