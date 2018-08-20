class EnvironmentModel:
    id: str
    parent: str
    data: dict
    name: str
    is_base: bool = False

    def __init__(self, env: dict):
        self.id = env['_id']
        self.parent = env['parentId']
        self.data = env['data']
        self.name = env['name']
        if self.parent.startswith('wrk_'):
            self.is_base = True
