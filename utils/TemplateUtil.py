import os, yaml
from utils.FileUtil import FileUtil


class TemplateUtil:
    @staticmethod
    def readTemplate(templateFilePath):
        try:
            f_template = open(templateFilePath, 'r')
            template_content = yaml.load(f_template, Loader=yaml.FullLoader)
            return template_content
        except FileNotFoundError:
            print("Template not found!!")

    @staticmethod
    def readRequestTemplate(templateFilePath):
        yaml_content = TemplateUtil.readTemplate(templateFilePath)
        requests_content = yaml_content['requests'][0]
        return requests_content

    @staticmethod
    def readInfoTemplate(templateFilePath):
        yaml_content = TemplateUtil.readTemplate(templateFilePath)
        info_content = yaml_content['info']
        return info_content

    # return payload value
    @staticmethod
    def readPayloadsField(templateFilePath):
        yaml_content = TemplateUtil.readTemplate(templateFilePath)
        requests_content = yaml_content['requests'][0]
        payloadListFromTemplate = requests_content['payloads']
        payloadDict = {}
        for payload in payloadListFromTemplate:
            for payloadKey in payload:
                payloadValue = payload[payloadKey]
                if type(payloadValue) is list:
                    payloadDict[payloadKey] = payload[payloadKey]
                if type(payloadValue) is str:   # payloadValue here is file path
                    payloadValueFromFile = FileUtil.readPayloadFromFile(payloadValue)
                    payloadDict[payloadKey] = payloadValueFromFile
        # print("[Debug] - Payload final dict:" + str(payloadDict))
        return payloadDict





