import json
from parsers.export_parser import ExportParser
from interfaces.terminal import TerminalInterface
from sunit.runner import TestRunner


def main():
    _raw: str
    with open('test_export.json', encoding="utf8") as file:
        _raw = file.read()
    parser = ExportParser(json.loads(_raw))
    interface = TerminalInterface()
    runner = TestRunner(export_parser=parser, environment_name='sahand', interface=interface)
    interface.start()


if __name__ == '__main__':
    main()
