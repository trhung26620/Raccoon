
class Payload:
    def __init__(self, payloadValues):
        self.payloadValue = payloadValues

    def getPayloadValueByKey(self, key):
        payload = self.payloadValues
        return payload[key]




