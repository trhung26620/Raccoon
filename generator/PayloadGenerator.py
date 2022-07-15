from models.Payload import Payload
from utils.TemplateUtil import TemplateUtil


class PayloadGenerator:

    @staticmethod
    def generatePayloadObjFromTemplate(templateFilePath):
        payloadDict = TemplateUtil.readPayloadsField(templateFilePath)
        if payloadDict is None:
            return None
        for k,v in payloadDict.items():
            if v:
                for index in range(len(v)):
                    payloadDict[k][index] = str(payloadDict[k][index])
        resultPayloads = Payload(payloadDict)
        return resultPayloads

