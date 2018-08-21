from typing import List, Any
import json


class BodyModel:
    type: str
    body: Any = None

    def __init__(self, body: dict):
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

    def is_form(self) -> bool:
        return self.type == 'form'

    def get_form(self) -> List[dict]:
        return self.body


class RequestModel:
    id: str
    body: BodyModel = None
    headers: dict = {}
    method: str
    name: str
    parent: str
    url: str
    order: float

    def __init__(self, request: dict):
        self.id = request['_id']
        self.body = BodyModel(request['body'])
        for header in request['headers']:
            self.headers[header['name']] = header['value']
        self.method = request['method']
        self.name = request['name']
        self.parent = request['parentId']
        self.url = request['url']
        self.order = request['metaSortKey']
