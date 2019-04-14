import json
from parsers.export_parser import ExportParser
from interfaces.terminal import TerminalInterface
from sunit.runner import TestRunner
import sys


def main():
    _raw: str
    args = sys.argv
    file = args[1]
    env = args[2]
    no_color = args[3]
    with open(file, encoding="utf8") as file:
        _raw = file.read()
    parser = ExportParser(json.loads(_raw))
    interface = TerminalInterface()
    interface.no_color = args[3] == "true"
    runner = TestRunner(export_parser=parser, environment_name=env, interface=interface)
    interface.start()


if __name__ == '__main__':
    main()
