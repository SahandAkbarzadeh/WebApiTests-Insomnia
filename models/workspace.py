from typing import List, Dict, Type
from .request import RequestModel
from .environment import EnvironmentModel


class WorkspaceModel:
    requests: List[RequestModel] = []
    environments: List[EnvironmentModel] = []
    name: str
    id: str
    description: str

    def __init__(self, workspace: dict, requests=None, environments: [EnvironmentModel] = None):
        self.environments = []
        self.requests = []
        if requests is None:
            requests = []
        self.name = workspace['name']
        self.id = workspace['_id']
        self.description = workspace['description']

        self.requests = [] if requests is None else requests
        self.environments = [] if environments is None else environments
