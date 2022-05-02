class Request:
    def __init__(self, url, header, body, position):
        self.url = url
        self.header = header
        self.body = body
        self.position = position