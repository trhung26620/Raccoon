from config.StaticData import DefaultConfigMatcher

class Matcher:
    def __init__(self, type, signature, part, condition, negative):
        self.type = self.checkValidType(type)
        self.signature = signature
        self.part = self.checkValidPart(part)
        self.condition = condition
        self.negative = negative

    def checkValidType(self, type):
        validType = ["word", "regex", "dsl","status", "size"]
        if type in validType:
            return type
        else:
            return DefaultConfigMatcher.defaultType

    def checkValidPart(self, part):
        validPart = ["header", "body", "all"]
        if part in validPart:
            return part
        else:
            return DefaultConfigMatcher.defaultPart