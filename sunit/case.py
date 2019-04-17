from typing import List, Union, Optional
from models.request import RequestModel
from models.report import Report
from logger.logger import Logger
from parsers.environment_variable_parser import EnvironmentVariableParser
from requests import request

from sunit.variable_save import VariableSave
from .expect_solver import ExpectSolver


class TestCase:
    _name: str
    _enabled: bool
    _expressions: List[ExpectSolver]

    _headers_add: Optional[dict]
    _headers_remove: Optional[list]
    _headers_ignore_defaults: Optional[dict]
    _headers: dict

    _body_add: Union[str, dict, None]
    _body_remove: Union[str, list, None]
    _body_ignore_default: Union[str, dict, None]
    _body: dict

    _save: [VariableSave]

    _tags: [str]

    _request_model: Optional[RequestModel]

    _environment: Optional[EnvironmentVariableParser]

    _reports: List[Report]

    def __init__(self, __test__: dict, request_model: RequestModel, environment: EnvironmentVariableParser):
        # setting default values
        self._name = ''
        self._reports = []
        self._environment = None
        self._enabled = True
        self._expressions = None
        self._request_model = None
        self._headers_add = None
        self._headers_remove = None
        self._headers_ignore_defaults = None
        self._headers = {}
        self._body_add = None
        self._body_remove = None
        self._body_ignore_default = None
        self._body = {}
        self._tags = []
        # request model will be useful with url, request mode, naming, ...
        self._request_model = request_model
        # environment will be useful for default headers
        self._environment = environment

        # parse __test__ to fill properties

        # name
        _name = __test__.get('name', '')
        if _name == '':
            self._name = self._request_model.name + '@' + self.generate_name()
        else:
            self._name = _name

        # enabled
        _data = __test__.get('enabled', True)
        if type(_data) is not bool:
            Logger.get().debug('[TestCase]',
                               'expected bool got {0}'.format(type(_data)),
                               'for:',
                               str(_data))
            _data = True
        self._enabled = self._request_model.tests_enabled and _data

        # body
        # TODO: add type validation for body
        self._body_add = __test__.get('+b', None)
        self._body_remove = __test__.get('-b', None)
        self._body_ignore_default = __test__.get('b', None)

        # create current body
        # TODO: add validation to check if body is json
        _body = self._request_model.body.get_json_for_request()

        # check if current body is ignored
        if self._body_ignore_default is None:
            # add extra body elements
            if self._body_add is not None:
                _body.update(self._body_add)
            # remove elements from default body ( and elements added in via _body_add)
            if self._body_remove is not None:
                for element in self._body_remove:
                    if type(element) is str:
                        if _body.get(element, None) is not None:
                            del _body[element]
                    else:
                        Logger.get().debug('[TestCase]',
                                           '-b must be list of string but an element is {0}'.format(type(element)))
        else:
            _body = self._body_ignore_default
        self._body = _body

        # headers
        # TODO: add type validation for headers
        self._headers_add = __test__.get('+h', None)
        self._headers_remove = __test__.get('-h', None)
        self._headers_ignore_defaults = __test__.get('h', None)

        _headers = self._request_model.headers

        # check if current headers is ignored
        if self._headers_ignore_defaults is None:
            # check for insomnia DEFAULT_HEADERS plugin
            _DEFAULT_HEADERS = self._environment.get('DEFAULT_HEADERS', None)

            if _DEFAULT_HEADERS is not None:
                assert isinstance(_DEFAULT_HEADERS, dict)
                _temp = _DEFAULT_HEADERS.copy()
                _temp.update(_headers.copy())
                _headers = _temp

            # add extra header elements
            if self._headers_add is not None:
                _headers.update(self._headers_add)
            # remove elements from default headers ( and elements added in via _headers_add)
            if self._headers_remove is not None:
                for element in self._headers_remove:
                    if type(element) is str:
                        if _body.get(element, None) is not None:
                            del _headers[element]
                    else:
                        Logger.get().debug('[TestCase]',
                                           '-h must be list of string but an element is {0}'.format(type(element)))
        else:
            _headers = self._headers_ignore_defaults
        self._headers = _headers

        # tags
        self._tags = __test__.get('tags', [])
        self._tags += self._request_model.tests_tags

        # expression
        _expressions = __test__.get('expects', [])
        self._expressions = []
        for expr in _expressions:
            if type(expr) is str:
                self._expressions.append(ExpectSolver(expr))
            elif type(expr) is dict:
                for key in expr:
                    self._expressions.append(ExpectSolver(expr[key], name=key))
            else:
                Logger.get().debug('[TestCase]',
                                   'expect case must be either str or dict but is {0}'.format(type(expr)))

        # save variables
        _save = __test__.get('save', [])
        self._save = []
        for save in _save:
            if type(save) is str:
                self._save.append(VariableSave(save))
            else:
                Logger.get().debug('[TestCase]',
                                   'save variables must be str but is {0}'.format(type(save)))

    # noinspection PyBroadException
    def run(self):
        # TODO : this only supports json add more

        # send request
        try:
            _response = request(
                self._request_model.method,
                self._request_model.url,
                headers=self._headers,
                json=self._body,
            )
            self._reports.append(Report(True, '', name=self._name, tag='main'))

        except Exception as e:
            self._reports.append(Report(False, str(e), name='sending request ' + self._name, tag='main'))
            # create N/A reports for expressions
            for expr in self._expressions:
                self._reports.append(Report(None, 'expression ignored', name=expr.name, tag='sub'))
            return

        # check expects
        for expr in self._expressions:
            expr.request_response = _response
            expr.solve()
            self._reports.append(Report(expr.ok, 'pass' if expr.ok else expr.error, name=expr.name, tag='sub'))

        for save in self._save:
            save.request_response = _response
            save.solve()

    @property
    def ok(self):
        _ok = True
        for report in self._reports:
            if report.status is False:
                _ok = False
                break
            if report.status is None:
                _ok = None
                break
        return _ok

    def report(self):
        return self._reports

    def generate_name(self):
        return '[{0}]{1}@{2}'.format(
            self._request_model.method,
            self._request_model.name,
            self._request_model.url
        )
