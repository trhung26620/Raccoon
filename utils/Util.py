from urllib.parse import urlparse
import os.path

class Util:
    def __init__(self):
        self.args = None
    
    def findAndReplaceURLPattern(self,givenStr, findStr, repStr):
        if givenStr.find(findStr) > -1: #Nếu if này không xảy ra thì hàm trả về cái gì? (chưa xử lý)
            o = urlparse(repStr)
        
            if(findStr == '{{BaseURL}}'):
                return givenStr.replace(findStr,repStr)
            elif(findStr == '{{RootURL}}'):
                return givenStr.replace(findStr,o.scheme + "://" + o.netloc)
            elif(findStr == '{{Hostname}}'):
                return givenStr.replace(findStr,o.netloc)
            elif(findStr == '{{Host}}'):
                return givenStr.replace(findStr,o.hostname)
            elif(findStr == '{{Port}}'):
                return givenStr.replace(findStr,o.port)
            elif(findStr == '{{FullPath}}'):
                return givenStr.replace(findStr,o.path + "?" + o.query)
            elif(findStr == '{{Path}}'):
                path = os.path.split(o.path)[0]
                return givenStr.replace(findStr,path)
            elif(findStr == '{{File}}'):
                file = os.path.split(o.path)[1]
                return givenStr.replace(findStr,file)
            elif(findStr == '{{Scheme}}'):
                return givenStr.replace(findStr,o.scheme)

            # Trường hợp người dùng nhập các pattern sai những cái định sẵn thì hàm trả về cái gì? (chưa xử lý)
