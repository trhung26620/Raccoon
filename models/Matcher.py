from config.StaticData import DefaultConfigMatcher, Template
from utils.TemplateUtil import TemplateUtil

class Matcher:
    def __init__(self, type, signature, part, condition, negative, reqCondition):
        self.reqCondition = reqCondition
        self.type = self.checkValidType(type)
        self.signature = signature
        self.part = self.checkValidPart(part)
        self.condition = condition
        self.negative = negative

    def checkValidType(self, type):
        validType = ["word", "regex", "status", "time"]
        if type in validType:
            return type
        else:
            return DefaultConfigMatcher.defaultType

    def checkValidPart(self, part):
        defaultValidPart = ["header", "body", "all", "interactsh_protocol", "interactsh_request", "interactsh_response"]
        validPart = defaultValidPart.copy()
        if self.reqCondition:
            numberOfRequests = len(TemplateUtil.readRequestTemplate(Template.templatePath)["request"])
            for defaultValid in defaultValidPart:
                for i in range(numberOfRequests):
                    validPart.append(defaultValid + "_" + str(i+1))
        if part in validPart:
            return part
        elif self.reqCondition:
            return None
        elif not self.reqCondition:
            return DefaultConfigMatcher.defaultPart