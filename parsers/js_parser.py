from typing import List
import re
from .environment_variable_parser import EnvironmentVariableParser
from .functions.ray_token_gen import ray_token_gen


class MethodEvaluator:
    parameters: List[str]

    def __init__(self, body: str, environment_parser: EnvironmentVariableParser):
        self.parameters = []
        self.environment_parser = environment_parser
        self.body = body.strip()
        self._parse_parameters()

    def _get_method_name(self):
        return str(self.body.split(' ')[0]).strip()

    def _parse_parameters(self):
        _raw = ''.join(self.body.split(' ')[1:])
        _par = _raw.split(',')
        for parameter in _par:
            if parameter.startswith("'") and parameter.endswith("'"):
                self.parameters.append(parameter.strip("'"))
            elif parameter.isnumeric():
                self.parameters.append(str(parameter))
            else:
                val = self.environment_parser.get(str(parameter))
                if val is not None:
                    self.parameters.append(val)
                else:
                    self.parameters.append('')

    def eval(self) -> str:
        _method_name = self._get_method_name()
        if _method_name == ray_token_gen.__js_name__:
            ray_token_gen(
                self.environment_parser.get('KEYGEN_SECRET', default=''),
                self.environment_parser.get('KEYGEN_SALT', default=''),
                self.parameters[0],
                self.parameters[1],
                self.parameters[2],
            )
        else:
            return ''


class JsParser:
    environment_parser: EnvironmentVariableParser

    __get_variables_pattern = re.compile(r"{{(.*?)}}")
    __get_methods_pattern = re.compile(r"{%(.*?)%}")

    def __init__(self, environment_parser: EnvironmentVariableParser):
        self.environment_parser = None
        self.environment_parser = environment_parser
        self.parse()

    def parse(self):
        for _ in range(5):
            self._iter_parser()
        for environment in self.environment_parser.environments:
            print(environment.data)

    def _iter_parser(self):
        for environment in self.environment_parser.environments:
            self._parse_dict(environment.data)

    def _parse_dict(self, env_dict: dict):
        for key in env_dict:
            if type(env_dict[key]) is str:
                variables = JsParser.get_variables(env_dict[key])
                for variable in variables:
                    value = self.environment_parser.get(variable)
                    if value is not None:
                        JsParser.set_variable(
                            variable,
                            value,
                            env_dict,
                            key)
                methods = JsParser.get_methods(env_dict[key])
                for method in methods:
                    JsParser.set_method(
                        method,
                        MethodEvaluator(method, self.environment_parser).eval(),
                        env_dict,
                        key
                    )
            elif type(env_dict[key]) is dict:
                self._parse_dict(env_dict[key])

    @staticmethod
    def get_variables(value: str) -> List[str]:
        matches = JsParser.__get_variables_pattern.findall(value)
        if matches:
            variables = []
            for match in matches:
                variables.append(str(match).strip())
            return variables
        else:
            return []

    @staticmethod
    def set_variable(key: str, value: str, in_dict: dict, dict_key: str):
        to_match = in_dict[dict_key]
        matches = JsParser.__get_variables_pattern.findall(to_match)
        if matches:
            for match in matches:
                if str(match).strip() == key:
                    in_dict[dict_key] = in_dict[dict_key].replace('{{' + str(match) + '}}', value)

    @staticmethod
    def get_methods(value: str) -> List[str]:
        matches = JsParser.__get_methods_pattern.findall(value)
        if matches:
            methods = []
            for match in matches:
                methods.append(str(match).strip())
            return methods
        else:
            return []

    @staticmethod
    def set_method(key: str, value: str, in_dict: dict, dict_key: str):
        to_match = in_dict[dict_key]
        matches = JsParser.__get_methods_pattern.findall(to_match)
        if matches:
            for match in matches:
                if str(match).strip() == key:
                    in_dict[dict_key] = in_dict[dict_key].replace('{%' + str(match) + '%}', value)
