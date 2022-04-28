import yaml
from utils.TemplateUtil import TemplateUtil
from models.TemplateConfig import TemplateConfig
from config.StaticData import DefaultTemplateConfig, DefaultConfigMatcher, DefaultConfigExtractor
from generator.PayloadGenerator import PayloadGenerator
from utils.ConfigUtil import ConfigUtil
from services.InteractShService import InteractSh
from models.Matcher import Matcher
from models.Extractor import Extractor

class TemplateConfigService:
    @staticmethod
    def getObjTemplateConfigByTemplate(templateFilePath):
        templateRequest = TemplateUtil.readRequestTemplate(templateFilePath)
        configYml = ConfigUtil.readConfig()
        try:
            if "redirect" in templateRequest:
                redirect = templateRequest["redirect"]
            else:
                redirect = DefaultTemplateConfig.defaultRedirect

            if "stopAtFirstMatch" in templateRequest:
                stopAtFirstMatch = templateRequest["stopAtFirstMatch"]
            else:
                stopAtFirstMatch = DefaultTemplateConfig.defaultStopAtFirstMatch
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
            if "matchers-condition" in templateRequest:
                matchers_condition = templateRequest["matchers-condition"].lower()
            else:
                matchers_condition = DefaultTemplateConfig.defaultMatchersCondition
            payload = PayloadGenerator.generatePayloadObjFromTemplate(templateFilePath)
            objTemplateConfig = TemplateConfig(redirect, payload, thread, scanMode, interactSh, stopAtFirstMatch, cookieReuse, matchers_condition)
            return objTemplateConfig
        except yaml.YAMLError as error:
            print("[Debug - TemplateConfigService] Error: " + error)

    @staticmethod
    def generateMatcherObjectList(templateFilePath):
        templateRequest = TemplateUtil.readRequestTemplate(templateFilePath)
        matcherList = templateRequest["matchers"]
        matcherObjectList = list()
        for matcher in matcherList:
            if "type" in matcher:
                type = matcher["type"]
                if type in matcher:
                    signature = matcher[type]
                else:
                    signature = DefaultConfigMatcher.defaultSignature
            else:
                type = DefaultConfigMatcher.defaultType
                signature = DefaultConfigMatcher.defaultSignature
            if "part" in matcher:
                part = matcher["part"]
            else:
                part = DefaultConfigMatcher.defaultPart
            if "condition" in matcher:
                condition = matcher["condition"]
            else:
                condition = DefaultConfigMatcher.defaultCondition
            if "negative" in matcher:
                negative = matcher["negative"]
            else:
                negative = DefaultConfigMatcher.defaultNegative
            matcherObj = Matcher(type, signature, part, condition, negative)
            matcherObjectList.append(matcherObj)
        return matcherObjectList

    @staticmethod
    def generateExtractorObjectList(templateFilePath):
        templateRequest = TemplateUtil.readRequestTemplate(templateFilePath)
        extractorList = templateRequest["extractors"]
        extractorObjectList = list()
        for extractor in extractorList:
            if "type" in extractor:
                type = extractor["type"]
                if type in extractor:
                    signature = extractor[type]
                else:
                    signature = DefaultConfigExtractor.defaultSignature
            else:
                type = DefaultConfigExtractor.defaultType
                signature = DefaultConfigExtractor.defaultSignature
            if "part" in extractor:
                part = extractor["part"]
            else:
                part = DefaultConfigExtractor.defaultPart
            if "internal" in extractor:
                internal = extractor["internal"]
            else:
                internal = DefaultConfigExtractor.defaultInternal
            if "group" in extractor:
                group = extractor["group"]
            else:
                group = DefaultConfigExtractor.defaultGroup
            extractorObj = Extractor(type, signature, part, internal, group)
            extractorObjectList.append(extractorObj)
        return extractorObjectList




