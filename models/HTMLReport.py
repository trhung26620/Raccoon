class HTMLReport:
    def __init__(self, target, templateFilePath, exposer, injectedPayload):
        self.target = target
        self.templateFilePath = templateFilePath
        self.exposer = exposer
        self.injectedPayload = injectedPayload
