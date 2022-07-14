import os, yaml
from utils.FileUtil import FileUtil
from utils.PrinterUtil import Printer

class TemplateUtil:
    @staticmethod
    def readTemplate(templateFilePath):
        try:
            f_template = open(templateFilePath, 'r')
            template_content = yaml.load(f_template, Loader=yaml.FullLoader)
            return template_content
        except FileNotFoundError:
            Printer.printError("Can not find path: '" + templateFilePath)
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


    @staticmethod
    def getTemplateSeverity(templateFilePath):
        info = TemplateUtil.readInfoTemplate(templateFilePath)
        if "severity" in info:
            severity = info["severity"]
            return severity
        Printer.printError("Template: " + templateFilePath + " does not has severity tag!")
        return None







