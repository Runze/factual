from .base import Base

class Write(Base):
    def __init__(self, api, table, factual_id, params):
        self.table = table
        self.factual_id = factual_id
        Base.__init__(self, api, self._path(), params, 'POST')

    def write(self):
        return self.api.post(self)

    def factual_id(self, factual_id):
        self.factual_id = factual_id
        self.path = self._path()

    def user(self, user):
        return self._copy({'user': user})

    def comment(self, comment):
        return self._copy({'comment': comment})

    def reference(self, reference):
        return self._copy({'reference': reference})

    def _path(self):
        pass

    def _copy(self, params):
        pass
