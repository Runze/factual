from .write import Write

class Boost(Write):
    def __init__(self, api, table, factual_id, params):
        Write.__init__(self, api, table, factual_id, params)

    def _path(self):
        return 't/{0}/boost'.format(self.table)

    def _copy(self, params):
        return Boost(self.api, self.table, self.factual_id, self.merge_params(params))
