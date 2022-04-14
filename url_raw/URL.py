import sys
sys.path.insert(0, 'Injection-Tool')
from utils import TemplateUtil, CommandUtil, Util
class URL:
    def __init__(self, schema, method, host, port, path, paramPath):
        self.schema = schema
        self.method = method
        self.host = host
        self.port = port
        self.path = path
        self.paramPath = paramPath

    def getInformationFromUser():
        print(TemplateUtil.readTemplate())



URL.getInformationFromUser()