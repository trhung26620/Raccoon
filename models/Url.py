class Url:
    def __init__(self, schema, method, host, path, paramPath):
        self.schema = schema
        self.method = method
        self.host = host
        self.path = path
        self.paramPath = paramPath