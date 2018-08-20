import json

from logger.logger import Logger


class ExportParser:
    _raw: json

    def __init__(self, data: json):
        self._raw = data
        self.parse()

    def parse(self):
        _environments = [x for x in self._raw['resources'] if x['_type'] == 'environment']
        _requests = [x for x in self._raw['resources'] if x['_type'] == 'request']
        Logger.get().debug('test')