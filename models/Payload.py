
class Payload:
    def __init__(self, filePath, payloadValue):
        self.filePath = filePath
        self.payloadValue = payloadValue

    def getPayloadValueByKey(self, key):
        payload = self.payloadValue
        return payload[key]