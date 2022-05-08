import requests
from config.StaticData import DefaultRequestFiringConfig
from utils.ConfigUtil import ConfigUtil

class RequestHandle:
    @staticmethod
    def sendPostRequest(dataRequest, requestConfig, session=None):
        if requestConfig.cookieReuse and session:
            r = session.post(url=dataRequest["urlObj"].baseUrl, params=dataRequest["param"],
                             headers=dataRequest["header"], data=dataRequest["body"],
                             timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects=requestConfig.redirect)
            return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"]

        else:
            session = requests.Session()
            session.proxies.update(ConfigUtil.readConfig()["proxy"])
            session.verify = False
            session.allow_redirects = True
            r = session.post(url=dataRequest["urlObj"].baseUrl, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"],timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects = requestConfig.redirect)
            return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"]

    @staticmethod
    def sendGetRequest(dataRequest, requestConfig, session=None):
        if requestConfig.cookieReuse and session:
            r = session.get(url=dataRequest["urlObj"].baseUrl, params=dataRequest["param"],
                             headers=dataRequest["header"], data=dataRequest["body"],
                             timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects=requestConfig.redirect)
            return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"]
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.get(url=dataRequest["urlObj"].baseUrl, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"], timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects = requestConfig.redirect)

        return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"]

    @staticmethod
    def sendPutRequest(dataRequest, requestConfig):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.put(url=dataRequest["urlObj"].baseUrl, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"], timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects = requestConfig.redirect)
        return r, dataRequest["position"], dataRequest["id"]

    @staticmethod
    def sendDeleteRequest(dataRequest, requestConfig):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.delete(url=dataRequest["urlObj"].baseUrl, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"], timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects = requestConfig.redirect)
        return r, dataRequest["position"]

