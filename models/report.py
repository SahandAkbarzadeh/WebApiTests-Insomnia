from typing import Optional


class Report:
    name: str
    status: Optional[bool]
    description: str
    tag: str

    def __init__(self, status: Optional[bool], description: str = '', name: str = '', tag: str = ''):
        self.name = ''
        self.status = None
        self.description = ''
        self.tag = ''

        self.name = name
        self.status = status
        self.description = description
        self.tag = tag
