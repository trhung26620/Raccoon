class Extractor:
    def __init__(self, type, signature, part, internal, group):
        self.type = self.checkValidType(type)
        self.signature = signature
        self.part = self.checkValidPart(part)
        self.internal = internal
        self.group = group

    def checkValidType(self, type):
        validType = ["regex", "kval", "json", "xpath", "dsl", "interactsh_protocol", "interactsh_request", "interactsh_response"]
        if type in validType:
            return type
        else:
            return None

    def checkValidPart(self, part):
        validPart = ["header", "body", "all"]
        if part in validPart:
            return part
        else:
            return "all"

