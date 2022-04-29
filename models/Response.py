class Response:
    def __init__(self, status, header, body, time):
        self.status = status
        self.header = self.getRawHeader(header)
        self.body = body
        self.time = time
        self.headerAndBody = self.header + "\n" + self.body

    def getRawHeader(self, headerDict):
        raw_header = ""
        for k, v in headerDict.items():
            raw_header += str(k) + ": " + str(v) + "\n"
            raw_header = raw_header[:-1]
        return raw_header