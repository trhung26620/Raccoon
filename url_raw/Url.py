import sys
sys.path.append('.')
from utils import TemplateUtil, CommandUtil, Util
# from utils import *
class Url:
    # def __init__(self, schema, method, host, port, path, paramPath):
    #     self.schema = schema
    #     self.method = method
    #     self.host = host
    #     self.port = port
    #     self.path = path
    #     self.paramPath = paramPath
    def __init__(self) -> None:
        pass

    def received_From_User(self):
        test = TemplateUtil.TemplateUtil() 
        url_from_user = test.readConfigFile()['url'] #Hiện tại không có bên TemplateUtil - bổ sung sau (update 12h30 - 14/04)
        print(type(url_from_user))
        test1 = TemplateUtil.TemplateUtil().readRequestTemplate()
        print(test1[0])
        # request_from_template = TemplateUtil.readRequestTemplate()
        for req in test1:
            Util.Util().findAndReplaceURLPattern(req, '{{Hostname}}', test)


test2 = Url()
test2.received_From_User()


