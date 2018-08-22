from typing import List, Optional, Union
from logger.logger import Logger
import json


class BodyModel:
    type: str
    body: Union[dict, str, any]

    def __init__(self, body: dict):
        self.body = None
        _type = body.get('mimeType', 'unknown')

        if _type == 'application/json':
            self.type = 'json'
            try:
                self.body = json.loads(body['text'])
            except json.decoder.JSONDecodeError:
                self.body = body
                self.type = 'unknown'
        elif _type == 'multipart/form-data':
            self.body = 'form'
            self.body = body['params']
        else:
            self.type = 'unknown'
            self.body = body

    def is_json(self) -> bool:
        return self.type == 'json'

    def get_json(self) -> dict:
        return self.body

    def get_json_for_request(self) -> dict:
        body_copy = self.body.copy()
        if '__tests__' in body_copy:
            del body_copy['__tests__']
        if '__tests__enabled__' in body_copy:
            del body_copy['__tests__enabled__']
        if '__tags__' in body_copy:
            del body_copy['__tags__']
        return body_copy

    def is_form(self) -> bool:
        return self.type == 'form'

    def get_form(self) -> List[dict]:
        return self.body


class RequestModel:
    id: str
    body: BodyModel = None
    headers: dict
    method: str
    name: str
    parent: str
    url: str
    order: float

    _request: Optional[dict]

    def __init__(self, request: dict):
        self._request = None
        self._request = request
        self.headers = {}
        self.body = None
        self.id = request['_id']
        self.body = BodyModel(request['body'])
        for header in request['headers']:
            self.headers[header['name']] = header['value']
        self.method = request['method']
        self.name = request['name']
        self.parent = request['parentId']
        self.url = request['url']
        self.order = request['metaSortKey']

    @property
    def tests_tags(self) -> List[str]:
        if self.body.is_json():
            _data = self.body.get_json().get('__tags__', [])
            if type(_data) is not list:
                Logger.get().debug('[RequestModel]',
                                   'wrong __tags__ format expected list got {0}'.format(type(_data)),
                                   'for:',
                                   str(_data))
                return []
            # check if all records in __tags__ are string
            for tag in _data:
                if type(tag) is not str:
                    Logger.get().debug('[RequestModel]',
                                       'wrong tag format expected str got {0}'.format(type(tag)),
                                       'for:',
                                       str(tag))
                    return []
            return _data
        else:
            return []

    @property
    def tests_enabled(self) -> bool:
        if self.body.is_json():
            _data = self.body.get_json().get('__tests__enabled__', True)
            if type(_data) is not bool:
                Logger.get().debug('[RequestModel]',
                                   'wrong __tests__enabled__ format expected bool got {0}'.format(type(_data)),
                                   'for:',
                                   str(_data))
                return True
            # check if all records in __tags__ are string
            return _data
        else:
            return True
