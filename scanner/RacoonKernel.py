from concurrent.futures import ThreadPoolExecutor
from scanner.RequestHandle import RequestHandle
from scanner import PayloadInjection
from utils.ConfigUtil import ConfigUtil
import requests

class RacoonKernel:
    def runner(self, dataReqList, requestConfig):
        threads = []
        with ThreadPoolExecutor(max_workers=requestConfig.thread) as executor:
            for dataReq in dataReqList:
                threads.append(executor.submit(self.fireRequestsAndAnalyzeResponse, dataReq, requestConfig))

    def fireRequestsAndAnalyzeResponse(self, dataReq, requestConfig, session=None):
        if dataReq["urlObj"].method.lower() == "get":
            RequestHandle.sendGetRequest(dataReq, requestConfig, session)

        elif dataReq["urlObj"].method.lower() == "post":
            RequestHandle.sendPostRequest(dataReq, requestConfig, session)

        elif dataReq["urlObj"].method.lower() == "put":
            RequestHandle.sendPutRequest(dataReq, requestConfig)

        elif dataReq["urlObj"].method.lower() == "delete":
            RequestHandle.sendDeleteRequest(dataReq, requestConfig)

    def fireRequestWithCookieReuse(self, requestConfigObj, requestObjDict):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = True
        if requestConfigObj.payload:
            for url, requestObjList in requestObjDict.items():
                dataReqList = PayloadInjection.injectAllRawRequest(requestConfigObj, requestObjList)
                for dataReq in dataReqList:
                    self.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session)
        else:
            for url, requestObjList in requestObjDict.items():
                dataReqList = PayloadInjection.getDataRequestWithoutPayloads(requestObjList)
                for dataReq in dataReqList:
                    self.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session)

    def fireRequestWithMultiThread(self, requestConfigObj, requestObjDict):
        if requestConfigObj.payload:
            for url, requestObjList in requestObjDict.items():
                dataReqList = PayloadInjection.injectAllRawRequest(requestConfigObj, requestObjList)
                self.runner(dataReqList, requestConfigObj)
        else:
            for url, requestObjList in requestObjDict.items():
                dataReqList = PayloadInjection.getDataRequestWithoutPayloads(requestObjList)
                self.runner(dataReqList, requestConfigObj)

    def racoonFlowControl(self, requestConfigObj, requestObjDict):
        PayloadInjection.injectInteractShUrl(requestConfigObj, requestObjDict)
        if requestConfigObj.cookieReuse:
            self.fireRequestWithCookieReuse(requestConfigObj, requestObjDict)
        else:
            self.fireRequestWithMultiThread(requestConfigObj, requestObjDict)