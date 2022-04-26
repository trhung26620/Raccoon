class TemplateConfig:
    def __init__(self, redirect, payload, thread, scanMode, interactSh, stopAtFirstMatch, cookieReuse):
        self.redirect = redirect
        self.payload = payload
        self.thread = thread
        self.scanMode = scanMode
        self.interactSh = interactSh
        self.stopAtFirstMatch = stopAtFirstMatch
        if self.interactSh:
            self.interactShUrl = interactSh.registerInteractShServer()
        else:
            self.interactShUrl = None
        self.cookieReuse = cookieReuse


