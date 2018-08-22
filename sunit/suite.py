from .case import TestCase
from typing import List, Optional
from models.request import RequestModel
from parsers.environment_variable_parser import EnvironmentVariableParser
from models.report import Report


class TestSuite:
    _cases: List[TestCase]
    _name: str

    _request_model: Optional[RequestModel]
    _environment_parser: Optional[EnvironmentVariableParser]

    _reports: List[List[Report]]

    def __init__(self, name, request_model: RequestModel, environment_parser: EnvironmentVariableParser):
        self._request_model = None
        self._environment_parser = None
        self._reports = []

        self._name = name
        self._request_model = request_model
        self._environment_parser = environment_parser

    def add_case(self, __test__: dict):
        self._cases.append(TestCase(__test__, request_model=self._request_model, environment=self._environment_parser))

    def run(self):
        for case in self._cases:
            case.run()

    def report(self) -> List[List[Report]]:
        self._reports = []
        for case in self._cases:
            self._reports.append(case.report())
        return self._reports
