from .write import Write

class Insert(Write):
    def __init__(self, api, table, factual_id, params={}):
        Write.__init__(self, api, table, factual_id, params)

    def values(self, values):
        return self._copy({'values': values})

    def clear_blanks(self):
        return self._copy({'clear_blanks': True})

    def _path(self):
        path = 't/' + self.table
        if self.factual_id:
            path += '/' + self.factual_id
        path += '/insert'
        return path

    def _copy(self, params):
        return Insert(self.api, self.table, self.factual_id, self.merge_params(params))
