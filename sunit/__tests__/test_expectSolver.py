from unittest import TestCase
from requests.models import Response
from ..expect_solver import ExpectSolver


class TestExpectSolver(TestCase):

    def setUp(self):
        self.fake_response = Response()
        self.fake_response.encoding = 'UTF-8'
        self.fake_response._content = \
            b'''
            {
                "msg" :"Test",
                "status": 1
            }
            '''
        self.fake_response.status_code = 400
        self.expect_solver = ExpectSolver('', self.fake_response)

    def test_text_in_rs(self):
        self.expect_solver.expression = r"'test' in rs.lower()"
        self.assertTrue(self.expect_solver.solve())

    def test_text_not_in_rs(self):
        self.expect_solver.expression = r"'test' in rs.upper()"
        self.assertFalse(self.expect_solver.solve())

    def test_attr_in_json_dict(self):
        self.expect_solver.expression = r"r['msg'] == 'Test'"
        self.assertTrue(self.expect_solver.solve())

    def test_json_is_test(self):
        self.expect_solver.expression = r"r['msg'] is 'Test'"
        self.assertFalse(self.expect_solver.solve())

    def test_check_status_ok(self):
        self.expect_solver.expression = r"ok"
        self.assertFalse(self.expect_solver.solve())  # False because s is 400

    def test_check_status_code(self):
        self.expect_solver.expression = r"s == 400"
        self.assertTrue(self.expect_solver.solve())

    # TODO: Add h tests
    # TODO: Add hs tests
    # TODO: Add R tests
