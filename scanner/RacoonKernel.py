from concurrent.futures import ThreadPoolExecutor
from scanner.RequestHandle import RequestHandle
from scanner import PayloadInjection
from utils.ConfigUtil import ConfigUtil
from generator.ResponseGenerator import ResponseGenerator
from generator.TemplateConfigGenerator import TemplateConfigService
from utils.MatcherUtil import MatcherUtil
import requests

class RacoonKernel:
    def runner(self, dataReqList, requestConfig):
        threads = []
        with ThreadPoolExecutor(max_workers=requestConfig.thread) as executor:
            for dataReq in dataReqList:
                threads.append(executor.submit(self.fireRequestsAndAnalyzeResponse, dataReq, requestConfig))

    def hamTestSauNaySeXoa(self, r):
        filePath = r"D:\FPT LEARNING\Graduation Thesis\Scanner\Injection-Tool\template\demo template\addBodyJsonAndQueryToCVE44228.yaml"
        matcherObjList = TemplateConfigService.generateMatcherObjectList(filePath)
        extractorObjList = TemplateConfigService.generateExtractorObjectList(filePath)
        # print(matcherObjList)
        for matcherObj in matcherObjList:
            if matcherObj.type == "status":
                result = MatcherUtil.statusMatchResultList(r.status, matcherObj.signature)
                print(result)
                result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                print(result)
            # elif matcherObj.type == "word":
            if matcherObj.type == "word":
                result = MatcherUtil.wordMatchResultList(r, matcherObj.signature, matcherObj.part)
                result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                print(result)

    def fireRequestsAndAnalyzeResponse(self, dataReq, requestConfig, session=None):
        if dataReq["urlObj"].method.lower() == "get":
            try:
                r = RequestHandle.sendGetRequest(dataReq, requestConfig, session)
            except:
                r = None
            if r != None:
                resObj = ResponseGenerator.generateResponseObject(r)
                self.hamTestSauNaySeXoa(resObj)
            else:
                print("Muc tieu khong phan hoi")
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