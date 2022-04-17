from utils.TemplateUtil import TemplateUtil
from models.TemplateConfig import TemplateConfig
import StaticData


class TemplateConfigService:

    @staticmethod
    def getObjTemplateConfigByTemplate(templateFileName):
        templateRequest = TemplateUtil.readTemplate(templateFileName)

        redirect = templateRequest["redirect"]
        payload = templateRequest["payload"]
        thread = templateRequest["thread"]
        scanMode = templateRequest["scanMode"]
        interactShUrl = templateRequest["interactShUrl"]
        stopAtFirstMatch = templateRequest["stopAtFirstMatch"]

        # default value of these field if user not specify
        if redirect is None:
            redirect = StaticData.DefaultTemplateConfig.defaultRedirect
        if thread is None:
            thread = StaticData.DefaultTemplateConfig.defaultThread  # should be in Static Data
        if stopAtFirstMatch is None:
            stopAtFirstMatch = False
        if interactShUrl is None:   # because use OOB vector is optional so this field is nullable
            interactShUrl = ""

        objTemplateConfig = TemplateConfig(redirect, payload, thread, scanMode, interactShUrl, stopAtFirstMatch)
        return objTemplateConfig


