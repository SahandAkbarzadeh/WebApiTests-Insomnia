from .case import TestCase
from typing import List, Optional
from models.request import RequestModel
from parsers.environment_variable_parser import EnvironmentVariableParser
from models.report import Report


class TestSuite:
    _cases: List[TestCase]
    _name: str

    _environment_parser: Optional[EnvironmentVariableParser]

    _reports: List[List[Report]]

    def __init__(self, name, environment_parser: EnvironmentVariableParser):
        self._environment_parser = None
        self._reports = []

        self._name = name
        self._environment_parser = environment_parser

    def add_case(self, __test__: dict, model: RequestModel):
        self._cases.append(TestCase(__test__, request_model=model, environment=self._environment_parser))

    def runs(self):
        for case in self._cases:
            case.run()
            yield case.report()

    def report(self) -> List[List[Report]]:
        self._reports = []
        for case in self._cases:
            self._reports.append(case.report())
        return self._reports

    def report_min(self) -> List[Optional[bool]]:
        _min = []
        for case in self._cases:
            _min.append(case.ok)
        return _min

    @property
    def number_of_cases(self):
        return len(self._cases)
