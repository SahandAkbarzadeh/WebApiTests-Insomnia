from parsers.export_parser import ExportParser
from typing import Optional
from .suite import TestSuite
from .case import TestCase


class TestRunner:
    export_parser: Optional[ExportParser]
    _suite: TestSuite

    def __init__(self, export_parser: ExportParser, environment_name: str, interface):
        self.export_parser = None
        self._suite = None

        self.interface = interface
        self.export_parser = export_parser
        self.export_parser.environment_name = environment_name
        self.export_parser.parse()

        self.create_test_suites()

        # call backs
        self.interface.run_callback = self.interface_run

    def interface_run(self):
        self.run()

    def create_test_suites(self):
        self._suite = TestSuite(name='default', environment_parser=self.export_parser.environment_parser)
        for request in self.export_parser.requests:
            __tests__ = request.body.get_json().get('__tests__', [])
            for __test__ in __tests__:
                self._suite.add_case(__test__, request)

    def run(self):
        _cases_ran = 0
        for run in self._suite.runs():
            _cases_ran += 1
            self.interface.update(type='REPORT', data=run)
            self.interface.update(type='PROGRESS', data='{0}/{1}'.format(
                str(_cases_ran),
                str(self.number_of_cases())
            ))

    def number_of_cases(self):
        return self._suite.number_of_cases
