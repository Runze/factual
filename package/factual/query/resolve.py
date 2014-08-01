from .read import Read

class Resolve(Read):
    def __init__(self, api, table, values={}):
        Read.__init__(self, api, 't/' + table + '/resolve', values)

    def values(self, values):
        return self._copy({'values': values})

    def _copy(self, params):
        return Resolve(self.api, self.merge_params(params))
