"""
Multi read API call
"""

class Multi(object):
    def __init__(self, api, queries):
        self.api = api
        self.method = 'GET'
        self.path = 'multi'
        self.params = {}
        for key,val in queries.items():
            self.params[key] = api.build_multi_url(val)

    def make_request(self):
        return self.api.raw_read(self.path, {'queries':self.params})
