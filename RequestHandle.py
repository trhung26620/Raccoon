import requests


class RequestHandle:
    # def __init__(self):
    #     self.proxy
    #     self.timeout
    #     self.redirect
    @staticmethod
    def sendPostRequest(url, params, headers, body, HTTP_PROXY):
        session = requests.Session()
        session.proxies.update(HTTP_PROXY)
        session.verify = False
        session.allow_redirects = True
        r = session.post(url=url, params=params, headers=headers, data=body,timeout=10)
        return r

    @staticmethod
    def sendGetRequest(url, params, headers, body, HTTP_PROXY):
        session = requests.Session()
        session.proxies.update(HTTP_PROXY)
        session.verify = False
        session.allow_redirects = True
        r = session.get(url=url, params=params, headers=headers, data=body, timeout=10)
        return r