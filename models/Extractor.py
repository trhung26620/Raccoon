from config.StaticData import DefaultConfigExtractor

class Extractor:
    def __init__(self, type, signature, part, internal, group, attribute):
        self.type = self.checkValidType(type)
        self.signature = signature
        self.part = self.checkValidPart(part)
        self.internal = internal
        self.group = group
        self.attribute = attribute

    def checkValidType(self, type):
        validType = ["regex", "kval", "xpath", "dsl"]
        if type in validType:
            return type
        else:
            return DefaultConfigExtractor.defaultType

    def checkValidPart(self, part):
        validPart = ["header", "body", "all", "interactsh_protocol", "interactsh_request", "interactsh_response"]
        if part in validPart:
            return part
        else:
            return DefaultConfigExtractor.defaultPart

