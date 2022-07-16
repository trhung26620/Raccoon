import requests
from config.StaticData import DefaultRequestFiringConfig
from utils.ConfigUtil import ConfigUtil
from utils.PrinterUtil import Printer


class RequestHandle:
    @staticmethod
    def sendPostRequest(dataRequest, requestConfig, session=None):
        url = dataRequest["urlObj"].baseUrl.split(dataRequest["urlObj"].host)[0] + dataRequest["urlObj"].host + dataRequest["path"]
        if requestConfig.cookieReuse and session:
            r = session.post(url=url, params=dataRequest["param"],
                             headers=dataRequest["header"], data=dataRequest["body"],
                             timeout=int(ConfigUtil.readConfig()["timeout"]), allow_redirects=requestConfig.redirect)

            return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"], url

        else:
            session = requests.Session()
            session.proxies.update(ConfigUtil.readConfig()["proxy"])
            session.verify = False
            session.allow_redirects = True
            r = session.post(url=url, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"],timeout=int(ConfigUtil.readConfig()["timeout"]), allow_redirects = requestConfig.redirect)
            return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"], url

    @staticmethod
    def sendGetRequest(dataRequest, requestConfig, session=None):
        url = dataRequest["urlObj"].baseUrl.split(dataRequest["urlObj"].host)[0] + dataRequest["urlObj"].host + dataRequest["path"]
        if requestConfig.cookieReuse and session:
            r = session.get(url=url, params=dataRequest["param"],
                             headers=dataRequest["header"], data=dataRequest["body"],
                             timeout=int(ConfigUtil.readConfig()["timeout"]), allow_redirects=requestConfig.redirect)
            Printer.printInfo("Send GET to: " + dataRequest["urlObj"].baseUrl)
            return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"]
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.get(url=url, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"], timeout=int(ConfigUtil.readConfig()["timeout"]), allow_redirects = requestConfig.redirect)
        return r, dataRequest["position"], dataRequest["id"], dataRequest["payloadInfo"], url

    @staticmethod
    def sendPutRequest(dataRequest, requestConfig):
        url = dataRequest["urlObj"].baseUrl.split(dataRequest["urlObj"].host)[0] + dataRequest["urlObj"].host + dataRequest["path"]
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.put(url=url, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"], timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects = requestConfig.redirect)
        return r, dataRequest["position"], dataRequest["id"], url

    @staticmethod
    def sendDeleteRequest(dataRequest, requestConfig):
        url = dataRequest["urlObj"].baseUrl.split(dataRequest["urlObj"].host)[0] + dataRequest["urlObj"].host + dataRequest["path"]
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.delete(url=url, params=dataRequest["param"], headers=dataRequest["header"], data=dataRequest["body"], timeout=DefaultRequestFiringConfig.defaultTimeout, allow_redirects = requestConfig.redirect)
        return r, dataRequest["position"], url

