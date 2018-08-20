from typing import List
from models.environment import EnvironmentModel
from models.request import RequestModel
from models.workspace import WorkspaceModel
from logger.logger import Logger


class ExportParser:
    _raw: dict = {}
    environments: List[EnvironmentModel] = []
    requests: List[RequestModel] = []
    workspaces: List[WorkspaceModel] = []

    def __init__(self, data: dict):
        self._raw = data
        self.parse()

    def parse(self):
        self._parse_environments()
        self._parse_requests()
        self._parse_workspaces()

    def _parse_environments(self):
        _environments = [x for x in self._raw['resources'] if x['_type'] == 'environment']
        for env in _environments:
            self.environments.append(EnvironmentModel(env))

    def _parse_requests(self):
        _requests = [x for x in self._raw['resources'] if x['_type'] == 'request']
        for req in _requests:
            self.requests.append(RequestModel(req))

    def _parse_workspaces(self):
        # TODO: Workspaces have no use
        _workspaces = [x for x in self._raw['resources'] if x['_type'] == 'workspace']
        for workspace in _workspaces:
            self.workspaces.append(WorkspaceModel(workspace))
