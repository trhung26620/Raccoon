import os, yaml
from utils import FileUtil


class TemplateUtil:
    @staticmethod
    def readTemplate(templateFilePath):
        try:
            f_template = open(templateFilePath, 'r')
            template_content = yaml.load(f_template, Loader=yaml.FullLoader)
            return template_content
        except FileNotFoundError:
            print("Template '" + templateFilePath+ "' not found!!")
            exit()

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

    @staticmethod
    def readPayloadsField(templateFilePath):
        yaml_content = TemplateUtil.readTemplate(templateFilePath)
        requests_content = yaml_content['requests'][0]
        try:
            payloadFromTemplate = requests_content['payloads']
            payloadDict = {}
            for payloadKey in payloadFromTemplate:
                payloadValue = payloadFromTemplate[payloadKey]
                if type(payloadValue) is list:
                    payloadDict[payloadKey] = payloadFromTemplate[payloadKey]
                if type(payloadValue) is str:
                    payloadValueFromFile = FileUtil.readPayloadFromFile(payloadValue)
                    payloadDict[payloadKey] = payloadValueFromFile
            return payloadDict
        except:
            return None







