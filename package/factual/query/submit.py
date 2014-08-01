from .write import Write

class Submit(Write):
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
        path += '/submit'
        return path

    def _copy(self, params):
        return Submit(self.api, self.table, self.factual_id, self.merge_params(params))
