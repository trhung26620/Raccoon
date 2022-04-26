class Url:
    def __init__(self, schema, method, host, path, paramPath, baseUrl):
        self.schema = schema
        self.method = method
        self.host = host
        self.path = path
        self.paramPath = paramPath
        self.baseUrl = baseUrl