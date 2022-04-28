class Response:
    def __init__(self, status, header, body, time):
        self.status = status
        self.header = header
        self.body = body
        self.time = time
        