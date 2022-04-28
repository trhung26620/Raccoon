from concurrent.futures import ThreadPoolExecutor
from scanner.RequestHandle import RequestHandle
from scanner import PayloadInjection
from utils.ConfigUtil import ConfigUtil
from generator.ResponseGenerator import ResponseGenerator
import requests

class RacoonKernel:
    def runner(self, dataReqList, requestConfig):
        threads = []
        with ThreadPoolExecutor(max_workers=requestConfig.thread) as executor:
            for dataReq in dataReqList:
                threads.append(executor.submit(self.fireRequestsAndAnalyzeResponse, dataReq, requestConfig))

    def fireRequestsAndAnalyzeResponse(self, dataReq, requestConfig, session=None):
        if dataReq["urlObj"].method.lower() == "get":
            try:
                r = RequestHandle.sendGetRequest(dataReq, requestConfig, session)
            except:
                r = None
            resObj = ResponseGenerator.generateResponseObject(r)
            if resObj:
                print(resObj.status)
                print("*" * 50)
                print(resObj.header)
                print("*" * 50)
                print(resObj.body)
                print("*" * 50)
                print(resObj.time)
            else:
                print("No data")
            # print(r.text)
            # print("*"*50)
            # print(r.headers)
            # print("*" * 50)
            # print(r.status_code)
            # print("*" * 50)
            # print(r.content)
            # print("*" * 50)
            # print(r.url)
            # print("*" * 50)
            # print(r.raw.read())
        elif dataReq["urlObj"].method.lower() == "post":
            r = RequestHandle.sendPostRequest(dataReq, requestConfig, session)

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