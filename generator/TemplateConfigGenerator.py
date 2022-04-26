import yaml

from utils.TemplateUtil import TemplateUtil
from models.TemplateConfig import TemplateConfig
from config.StaticData import DefaultTemplateConfig
from generator.PayloadGenerator import PayloadGenerator
from utils.ConfigUtil import ConfigUtil
from services.InteractShService import InteractSh
import json

class TemplateConfigService:

    @staticmethod
    def getObjTemplateConfigByTemplate(templateFilePath):
        templateRequest = TemplateUtil.readRequestTemplate(templateFilePath)
        # print(templateRequest)
        # print(json.dumps(templateRequest, sort_keys=False, indent=4))
        # exit()
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

            # if "interactShUrl" in templateRequest:   # because use OOB vector is optional so this field is nullable
            #     interactShUrl = templateRequest["interactShUrl"]
            # else:
            #     interactShUrl = DefaultTemplateConfig.defaultInteractShUrl
            for req in templateRequest["request"]:
                if "{{interactsh-url}}" in req:
                    interactSh = InteractSh()
                    break
                else:
                    interactSh = None
            if "scanMode" in templateRequest:
                scanMode = templateRequest["scanMode"]
            else:
                scanMode = DefaultTemplateConfig.defaultScanMode

            if configYml["thread"]:
                thread = configYml["thread"]
            elif "thread" in templateRequest:
                thread = templateRequest["thread"]
            else:
                thread = DefaultTemplateConfig.defaultThread
            if "cookieReuse" in templateRequest:
                cookieReuse = templateRequest["cookieReuse"]
            else:
                cookieReuse = DefaultTemplateConfig.defaultCookieReuse
            payload = PayloadGenerator.generatePayloadObjFromTemplate(templateFilePath)
            objTemplateConfig = TemplateConfig(redirect, payload, thread, scanMode, interactSh, stopAtFirstMatch, cookieReuse)
            return objTemplateConfig
        except yaml.YAMLError as error:
            print("[Debug - TemplateConfigService] Error: " + error)





