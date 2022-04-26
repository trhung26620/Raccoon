from concurrent.futures import ThreadPoolExecutor
from scanner.RequestHandle import RequestHandle
from scanner import RequestOperation

class RacoonKernel:
    @staticmethod
    def runner(dataReqList, requestConfig):
        threads = []
        with ThreadPoolExecutor(max_workers=requestConfig.thread) as executor:
            for dataReq in dataReqList:
                if dataReq["urlObj"].method.lower() == "get":
                    # for dataReq in dataReqList:
                    threads.append(executor.submit(RequestHandle.sendGetRequest, dataReq["urlObj"].baseUrl, dataReq["param"],
                                                       dataReq["header"], dataReq["body"]))
                elif dataReq["urlObj"].method.lower() == "post":
                    # for dataReq in dataReqList:
                    threads.append(executor.submit(RequestHandle.sendPostRequest, dataReq["urlObj"].baseUrl, dataReq["param"],
                                                       dataReq["header"], dataReq["body"]))
    @staticmethod
    def fireRequests(requestConfigObj, requestObjDict):
        for url, requestObjList in requestObjDict.items():
            dataReqList = RequestOperation.injectAllRawRequest(requestConfigObj, requestObjList)
            RacoonKernel.runner(dataReqList, requestConfigObj)