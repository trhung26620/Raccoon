import sys
import yaml
sys.path.append('../')
from utils.TemplateUtil import TemplateUtil
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
        pass
        # print(sys.path)
        # test = TemplateUtil.TemplateUtil() 
        # url_from_user = test.readConfigFile()['url'] #Hiện tại không có bên TemplateUtil - bổ sung sau (update 12h30 - 14/04)
        # test1 = TemplateUtil.TemplateUtil().readRequestTemplate()
        # print(test1[0])
        # request_from_template = TemplateUtil.readRequestTemplate()
        # for req in test1:
        #     # test3 = Util.Util().findAndReplaceURLPattern(req, '{{Hostname}}', url_from_user)
        #     print(test3)
        # print("\nAfter")
        # print(test1[0])

test2 = utils()
print(test2.readConfigFile())
test2.received_From_User()


