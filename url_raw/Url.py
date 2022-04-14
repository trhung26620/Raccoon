import sys
sys.path.insert(0, 'Injection-Tool')
from utils import TemplateUtil, CommandUtil, Util
import RequestHandle
class Url:
    def __init__(self, schema, method, host, port, path, paramPath):
        self.schema = schema
        self.method = method
        self.host = host
        self.port = port
        self.path = path
        self.paramPath = paramPath

    @classmethod # sử dụng: Url.received_From_User()
    def received_From_User():
        url_from_user = TemplateUtil.getConfigFile()['url'] #Hiện tại không có bên TemplateUtil - bổ sung sau (update 12h30 - 14/04)
        request_from_template = TemplateUtil.readRequestTemplate()
        for req in request_from_template:
            Util.findAndReplaceURLPattern(req, '{{Hostname}}', url_from_user)

        return Url()


