from .write import Write

class Flag(Write):
    def __init__(self, api, table, factual_id, params={}):
        Write.__init__(self, api, table, factual_id, params)

    def problem(self, problem, preferred=None):
        params = {'problem': problem}
        if preferred:
            params['preferred'] = preferred
        return self._copy(params)

    def duplicate(self, preferred=None):
        return self.problem('duplicate', preferred)

    def inaccurate(self):
        return self.problem('inaccurate')

    def nonexistent(self):
        return self.problem('nonexistent')

    def relocated(self, preferred=None):
        return self.problem('relocated', preferred)

    def inappropriate(self):
        return self.problem('inappropriate')

    def spam(self):
        return self.problem('spam')

    def other(self):
        return self.problem('other')

    def debug(self, debug):
        return self._copy({'debug': debug})

    def _path(self):
        return 't/{0}/{1}/flag'.format(self.table, self.factual_id)

    def _copy(self, params):
        return Flag(self.api, self.table, self.factual_id, self.merge_params(params))
