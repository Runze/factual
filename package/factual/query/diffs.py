"""
Factual Diffs API query
"""

from .base import Base

import json

class Diffs(Base):
    def __init__(self, api, path, start, end):
        self.cached_response = None
        Base.__init__(self, api, path, {'start':int(start), 'end':int(end)}, 'GET')

    def data(self):
        if not self.cached_response:
            raw_response = self.api.raw_read(self.path, self.params)
            self.cached_response = [json.loads(line) for line in raw_response.splitlines()]
        return self.cached_response

    def stream_raw(self):
        return self.api.raw_stream_read(self.path, self.params)

    def stream(self):
        for line in self.stream_raw():
            yield json.loads(line)
