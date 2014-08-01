from .write import Write

class Clear(Write):
    def __init__(self, api, table, factual_id, params={}):
        Write.__init__(self, api, table, factual_id, params)

    def fields(self, fields):
        return self._copy({'fields': fields})

    def _path(self):
        return 't/' + self.table + '/' + self.factual_id + '/clear'

    def _copy(self, params):
        return Clear(self.api, self.table, self.factual_id, self.merge_params(params))
