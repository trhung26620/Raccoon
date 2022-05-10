class HTMLReport:
    def __init__(self, templateFilePath, exposer, injectedPayload):
        self.templateFilePath = templateFilePath
        self.exposer = exposer
        self.injectedPayload = injectedPayload
