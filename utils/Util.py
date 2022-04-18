from urllib.parse import urlparse
import os.path
from utils.ConfigUtil import ConfigUtil

class Util:
    def findAndReplaceURLPattern(self, givenStr):
        config_content = ConfigUtil().readConfig()
        o = urlparse(config_content['url'])
        
        urlPattern = {
            '{{BaseURL}}': config_content['url'],
            '{{RootURL}}': o.scheme + "://" + o.netloc,
            '{{Hostname}}': o.netloc,
            '{{Host}}': o.hostname,
            '{{Port}}': str(o.port),
            '{{FullPath}}': o.path + "?" + o.query,
            '{{Path}}': os.path.split(o.path)[0],
            '{{File}}': os.path.split(o.path)[1],
            '{{Scheme}}': o.scheme
        }
        
        for k,v in urlPattern.items():
            givenStr = givenStr.replace(k,v)
        
        return givenStr
