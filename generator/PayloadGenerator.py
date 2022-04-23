from models.Payload import Payload
from utils.TemplateUtil import TemplateUtil


class PayloadGenerator:

    @staticmethod
    def generatePayloadObjFromTemplate(templateFilePath):
        payloadDict = TemplateUtil.readPayloadsField(templateFilePath)
        resultPayloads = Payload(payloadDict)
        return resultPayloads
