from models.Payload import Payload
from utils.TemplateUtil import TemplateUtil


class PayloadGenerator:

    @staticmethod
    def generatePayloadObjFromTemplate(templateFilePath):
        payloadDict = TemplateUtil.readPayloadsField(templateFilePath)
        if payloadDict is None:
            return None
        resultPayloads = Payload(payloadDict)
        return resultPayloads

