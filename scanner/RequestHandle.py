import requests
from config.StaticData import DefaultRequestFiringConfig
from utils.ConfigUtil import ConfigUtil

class RequestHandle:
    @staticmethod
    def sendPostRequest(url, params, headers, body):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = True
        r = session.post(url=url, params=params, headers=headers, data=body,timeout=DefaultRequestFiringConfig.defaultTimeout)
        return r

    @staticmethod
    def sendGetRequest(url, params, headers, body):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.get(url=url, params=params, headers=headers, data=body, timeout=DefaultRequestFiringConfig.defaultTimeout)
        return r

    @staticmethod
    def sendPutRequest(url, params, headers, body):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.put(url=url, params=params, headers=headers, data=body, timeout=DefaultRequestFiringConfig.defaultTimeout)
        return r

    @staticmethod
    def sendPutRequest(url, params, headers, body):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.delete(url=url, params=params, headers=headers, data=body, timeout=DefaultRequestFiringConfig.defaultTimeout)
        return r
