import yaml

from utils.TemplateUtil import TemplateUtil
from models.TemplateConfig import TemplateConfig
from config.StaticData import DefaultTemplateConfig
from generator.PayloadGenerator import PayloadGenerator
from utils.ConfigUtil import ConfigUtil


class TemplateConfigService:

    @staticmethod
    def getObjTemplateConfigByTemplate(templateFilePath):
        templateRequest = TemplateUtil.readRequestTemplate(templateFilePath)
        configYml = ConfigUtil.readConfig()
        try:
            # default value of these field if user not specify
            if "redirect" in templateRequest:
                redirect = templateRequest["redirect"]
            else:
                redirect = DefaultTemplateConfig.defaultRedirect

            if "stopAtFirstMatch" in templateRequest:
                stopAtFirstMatch = templateRequest["stopAtFirstMatch"]
            else:
                stopAtFirstMatch = DefaultTemplateConfig.defaultStopAtFirstMatch

            if "interactShUrl" in templateRequest:   # because use OOB vector is optional so this field is nullable
                interactShUrl = templateRequest["interactShUrl"]
            else:
                interactShUrl = DefaultTemplateConfig.defaultInteractShUrl

            if "scanMode" in templateRequest:
                scanMode = templateRequest["scanMode"]
            else:
                scanMode = DefaultTemplateConfig.defaultScanMode

            if "thread" in configYml:
                thread = configYml["thread"]

            payload = PayloadGenerator.generatePayloadObjFromTemplate(templateFilePath)
            objTemplateConfig = TemplateConfig(redirect, payload, thread, scanMode, interactShUrl, stopAtFirstMatch)
            return objTemplateConfig
        except yaml.YAMLError as error:
            print("[Debug - TemplateConfigService] Error: " + error)





