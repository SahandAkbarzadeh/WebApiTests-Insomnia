from models.report import Report
import sys

import colorama
from colorama import Back, Fore

colorama.init()


class TerminalInterface:
    no_color: bool = False
    minimal_output: bool = False

    def __init__(self):
        self.run_callback = None
        pass

    def start(self):
        if not self.no_color:
            colorama.init()
        else:
            Back.RESET = ''
            Fore.CYAN = ''
            Fore.RESET = ''
            Back.BLUE = ''
            Back.GREEN = ''
            Back.RED = ''
        self.run_callback()

    def update(self, update_type: str, data):
        if update_type == 'REPORT':
            for report in data:
                assert isinstance(report, Report)
                _prefix = ''
                if report.status and self.minimal_output:
                    continue
                if report.tag == 'sub':
                    if self.minimal_output and report.status:
                        continue
                    _prefix = '   '
                output = ''
                if self.no_color:
                    output = '{0}[{1}] {2} : {3}'.format(
                        _prefix,
                        '?' if report.status is None else 'P' if report.status is True else 'F',
                        report.name,
                        report.description
                    )
                else:
                    output = ('{0}{1}[{2}]' + Back.RESET + Fore.CYAN + '{3}' + Fore.RESET + ' :{4}').format(
                        _prefix,
                        Back.BLUE if report.status is None else Back.GREEN if report.status is True else Back.RED,
                        '?' if report.status is None else 'P' if report.status is True else 'F',
                        report.name,
                        report.description)
                output = TerminalInterface.fix_non_latin_chars(output)
                print(output)
        elif update_type == 'PROGRESS':
            pass
            # TODO: change terminal window title
        elif update_type == 'DONE':
            _passed = 0
            _failed = 0
            _ignored = 0
            for item in data:
                if item is True:
                    _passed += 1
                elif item is None:
                    _ignored += 1
                elif item is False:
                    _failed += 1
            print("""
            passed:\t {0}
            failed:\t {1}
            ignored:\t {2}
            total:\t {3}
            """.format(
                str(_passed),
                str(_failed),
                str(_ignored),
                str(_passed + _failed + _ignored)
            ))
            if _failed > 0:
                sys.exit(1)
            else:
                sys.exit(0)

    @staticmethod
    def fix_non_latin_chars(string):
        result = ''
        for value in string:
            if value in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890[]{}!#$%^&*()\\/`'\":\n\t -<>_=+-*/.":
                result += value
            else:
                result += '?'
        return result
