from .read import Read

class Match(Read):
    def __init__(self, api, table, values={}):
        Read.__init__(self, api, 't/' + table + '/match', values)

    def values(self, values):
        return self._copy({'values': values})

    def get_id(self):
        data = self.data()
        if len(data) > 0:
            return data[0]['factual_id']
        else:
            return None

    def _copy(self, params):
        return Match(self.api, self.merge_params(params))
