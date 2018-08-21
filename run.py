import json
from parsers.export_parser import ExportParser


def main():
    _raw: str
    with open('test_export.json', encoding="utf8") as file:
        _raw = file.read()
    parser = ExportParser(json.loads(_raw))
    _ = ''


if __name__ == '__main__':
    main()
