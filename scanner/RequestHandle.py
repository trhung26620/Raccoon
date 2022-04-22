import requests
from config.StaticData import DefaultRequestFiringConfig

class RequestHandle:
    @staticmethod
    def sendPostRequest(url, params, headers, body, HTTP_PROXY):
        session = requests.Session()
        session.proxies.update(HTTP_PROXY)
        session.verify = False
        session.allow_redirects = True
        r = session.post(url=url, params=params, headers=headers, data=body,timeout=DefaultRequestFiringConfig.defaultTimeout)
        return r

    @staticmethod
    def sendGetRequest(url, params, headers, body, HTTP_PROXY):
        session = requests.Session()
        session.proxies.update(HTTP_PROXY)
        session.verify = False
        session.allow_redirects = DefaultRequestFiringConfig.allow_redirect
        r = session.get(url=url, params=params, headers=headers, data=body, timeout=DefaultRequestFiringConfig.defaultTimeout)
        return r