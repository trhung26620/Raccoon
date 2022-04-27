from concurrent.futures import ThreadPoolExecutor
from scanner.RequestHandle import RequestHandle
from scanner import RequestOperation
from utils.ConfigUtil import ConfigUtil
import requests

class RacoonKernel:
    @staticmethod
    def runner(dataReqList, requestConfig):
        threads = []
        with ThreadPoolExecutor(max_workers=requestConfig.thread) as executor:
            for dataReq in dataReqList:
                threads.append(executor.submit(RacoonKernel.fireRequestsAndAnalyzeResponse, dataReq, requestConfig))

    @staticmethod
    def fireRequestsAndAnalyzeResponse(dataReq, requestConfig, session=None):
        if dataReq["urlObj"].method.lower() == "get":
            RequestHandle.sendGetRequest(dataReq, requestConfig, session)

        elif dataReq["urlObj"].method.lower() == "post":
            RequestHandle.sendPostRequest(dataReq, requestConfig, session)

        elif dataReq["urlObj"].method.lower() == "put":
            RequestHandle.sendPutRequest(dataReq, requestConfig)

        elif dataReq["urlObj"].method.lower() == "delete":
            RequestHandle.sendDeleteRequest(dataReq, requestConfig)

    @staticmethod
    def racoonFlowControl(requestConfigObj, requestObjDict):
        if requestConfigObj.cookieReuse:
            session = requests.Session()
            session.proxies.update(ConfigUtil.readConfig()["proxy"])
            session.verify = False
            session.allow_redirects = True
            if requestConfigObj.payload:
                for url, requestObjList in requestObjDict.items():
                    dataReqList = RequestOperation.injectAllRawRequest(requestConfigObj, requestObjList)
                    for dataReq in dataReqList:
                        RacoonKernel.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session)
            else:
                for url, requestObjList in requestObjDict.items():
                    dataReqList = RequestOperation.getDataRequestWithoutPayloads(requestObjList)
                    for dataReq in dataReqList:
                        RacoonKernel.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session)


        else:
            if requestConfigObj.payload:
                for url, requestObjList in requestObjDict.items():
                    dataReqList = RequestOperation.injectAllRawRequest(requestConfigObj, requestObjList)
                    RacoonKernel.runner(dataReqList, requestConfigObj)
            else:
                for url, requestObjList in requestObjDict.items():
                    dataReqList = RequestOperation.getDataRequestWithoutPayloads(requestObjList)
                    RacoonKernel.runner(dataReqList, requestConfigObj)