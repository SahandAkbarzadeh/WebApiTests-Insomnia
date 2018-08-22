from requests.models import Response
from typing import Optional


# noinspection PyBroadException
class ExpectSolver:
    expression: str  # str python expression to solve
    request_response: Optional[Response]  # request's response for solver's scope variables
    error: str

    _name: str

    __solver_response: Optional[bool]  #

    def __init__(self, expression: str, name: str=''):
        self._name = ''
        self.request_response = None
        self.expression = expression
        self.__solver_response = None
        self.error = ''
        self._name = name

    @property
    def name(self) -> str:
        if self._name == '':
            return self.expression
        else:
            return self._name

    def solve(self) -> bool:
        """
        evaluates python expression with given scope variables
        :return: assertion status
        """

        # expression's scope variables
        r = self.r  # response as json
        rs = self.request_response.text  # response as string
        h = self.request_response.headers  # headers as dict
        hs = str(h)  # headers as string
        s = self.request_response.status_code  # status code as int
        R = self.request_response  # response object
        ok = self.request_response.ok

        # runs python expression
        try:
            self.__solver_response = eval(self.expression)
        except Exception as e:
            self.__solver_response = False
            self.error = str(e)
        return self.ok

    @property
    def r(self) -> Optional[dict]:
        """
        json response
        :return: json or None
        """
        try:
            return self.request_response.json()
        except Exception as _:
            return None

    @property
    def ok(self) -> Optional[bool]:
        return self.__solver_response
