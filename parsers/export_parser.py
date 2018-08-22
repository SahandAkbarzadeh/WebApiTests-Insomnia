from typing import List, Optional
from models.environment import EnvironmentModel
from models.request import RequestModel
from models.workspace import WorkspaceModel
from models.request_group import RequestGroupModel
from .environment_variable_parser import EnvironmentVariableParser
from .js_parser import JsParser
from logger.logger import Logger


class ExportParser:
    _raw: dict = {}
    environments: List[EnvironmentModel] = []
    requests: List[RequestModel] = []
    workspaces: List[WorkspaceModel] = []
    request_groups: List[RequestGroupModel] = []
    environment_parser: Optional[EnvironmentVariableParser]
    environment_name: str

    def __init__(self, data: dict):
        self.environment_parser = None
        self._raw = data
        self.environment_name = ''

    def parse(self):
        self._parse_environments()
        self._parse_js()
        self._parse_request_groups()
        self._parse_requests()
        self._sort_requests_by_groups()

    def _parse_environments(self):
        _environments = [x for x in self._raw['resources'] if x['_type'] == 'environment']
        for env in _environments:
            self.environments.append(EnvironmentModel(env))

    def _parse_js(self):
        self.environment_parser = EnvironmentVariableParser(self.environments)
        self.environment_parser.selected_env = self.environment_parser.get_environment_by_name(self.environment_name)
        js_parser = JsParser(self.environment_parser)
        js_parser.parse(self._raw)

    def _parse_request_groups(self):
        _request_groups = [x for x in self._raw['resources'] if x['_type'] == 'request_group']
        _child_groups: List[RequestGroupModel] = []
        for req_group in _request_groups:
            _mdl = RequestGroupModel(req_group)
            if _mdl.in_root:
                self.request_groups.append(_mdl)
            else:
                _child_groups.append(_mdl)
        # detect child groups

        for child in _child_groups:
            for group in self.request_groups:
                if group.id == child.parent:
                    group.child_groups.append(child.id)
        # TODO: add support for more than depth-1 children
        for child in _child_groups:
            self.request_groups.append(child)
        # sort by meta sort key
        self.request_groups = sorted(self.request_groups, key=lambda grp: grp.order)
        pass

    def _parse_requests(self):
        _requests = [x for x in self._raw['resources'] if x['_type'] == 'request']
        for req in _requests:
            self.requests.append(RequestModel(req))

    def _sort_requests_by_groups(self):
        # put requests in groups
        _not_stated_requests: List[RequestModel] = []
        for _request in self.requests:
            position_stated = False
            _group = None
            for _group in self.request_groups:
                if _request.parent == _group.id or _request.parent in _group.child_groups:
                    position_stated = True
                    _group.requests.append(_request)
                    continue
            if not position_stated:
                _not_stated_requests.append(_request)
        # sort
        for _group in self.request_groups:
            _group.sort_requests()
        _not_stated_requests = sorted(_not_stated_requests, key=lambda req: req.order)
        # spread
        _temp_requests_container: [RequestModel] = []
        for _group in self.request_groups:
            for request in _group.requests:
                _temp_requests_container.append(request)
        for request in _not_stated_requests:
            _temp_requests_container.append(request)
        self.requests = _temp_requests_container
        pass

    def _parse_workspaces(self):
        """
            TODO: add workspaces support
        """
        _workspaces = [x for x in self._raw['resources'] if x['_type'] == 'workspace']
        for workspace in _workspaces:
            self.workspaces.append(WorkspaceModel(workspace))
