from typing import List, Optional, Union
from models.environment import EnvironmentModel


class EnvironmentVariableParser:
    base_environment: EnvironmentModel
    child_environments: List[EnvironmentModel]
    environments: List[EnvironmentModel]

    selected_env: EnvironmentModel

    def __init__(self, environments: List[EnvironmentModel]):
        self.child_environments = []
        self.environments = []
        self.base_environment = None

        self.environments = environments
        for env in environments:
            if env.is_base:
                self.base_environment = env
            else:
                self.child_environments.append(env)
        if self.base_environment is None:
            raise Exception('no base environment')

    def get(self, key: str, default=None) -> Union[str, dict, None]:
        """
        gets environment value from base and selected environment
        :param key:str
        :param default
        :return: value
        """
        _environment = self.selected_env
        if key in _environment.data:
            return _environment.data.get(key, '')
        if key in self.base_environment.data:
            return self.base_environment.data.get(key, '')
        return default

    def get_environment_by_name(self, name: str) -> Optional[EnvironmentModel]:
        for env in self.child_environments:
            if env.name == name:
                return env
        return None
