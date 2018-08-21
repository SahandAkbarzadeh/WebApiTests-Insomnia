from typing import List
from .request import RequestModel


class RequestGroupModel:
    id: str
    name: str
    parent: str
    order: float
    child_groups: List[str]
    in_root: bool = False
    requests: List[RequestModel] = []

    def __init__(self, request_group: dict):
        self.child_groups = []
        self.requests = []
        self.id = request_group['_id']
        self.name = request_group['name']
        self.parent = request_group['parentId']
        self.order = request_group['metaSortKey']
        if self.parent.startswith('wrk_'):
            self.in_root = True

    def sort_requests(self):
        self.requests = sorted(self.requests, key=lambda req: req.order)
