from concurrent.futures import ThreadPoolExecutor
from scanner.RequestHandle import RequestHandle
from scanner import PayloadInjection
from utils.ConfigUtil import ConfigUtil
from generator.ResponseGenerator import ResponseGenerator
from generator.TemplateConfigGenerator import TemplateConfigService
from utils.MatcherUtil import MatcherUtil
from config.StaticData import Template
import requests

class RaccoonKernel:
    def runner(self, dataReqList, requestConfig):
        threads = []
        with ThreadPoolExecutor(max_workers=requestConfig.thread) as executor:
            for dataReq in dataReqList:
                threads.append(executor.submit(self.fireRequestsAndAnalyzeResponse, dataReq, requestConfig))
        futureList = list()
        for future in threads:
            futureList.append(future.result())
        return futureList

    def matcherProcess(self, response, requestConfig):
        matcherObjList = TemplateConfigService.generateMatcherObjectList(Template.templatePath, requestConfig.reqCondition)
        matcherResultList = list()
        # dataList = None
        # if requestConfig.interactSh:
        #     dataInteractsh, aes_key = requestConfig.interactSh.pollDataFromWeb()
        #     if aes_key:
        #         key = requestConfig.interactSh.decryptAESKey(aes_key)
        #         dataList = requestConfig.interactSh.decryptMessage(key, dataInteractsh)
        defaultPart = ["header", "body", "all", "interactsh_protocol", "interactsh_request", "interactsh_response"]
        for matcherObj in matcherObjList:
            if matcherObj.part:
                if matcherObj.part in defaultPart or str(response.position) == matcherObj.part.split("_")[1]:
                    if matcherObj.type == "status":
                        result = MatcherUtil.statusMatchResultList(response.status, matcherObj.signature)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
                    elif matcherObj.type == "word":
                        result = MatcherUtil.wordMatchResultList(response, matcherObj.signature, matcherObj.part, requestConfig.interactSh)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
                    elif matcherObj.type == "time":
                        result = MatcherUtil.timeMatchResultList(response.time, matcherObj.signature)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
                    elif matcherObj.type == "regex":
                        result = MatcherUtil.regexMatchResultList(response, matcherObj.signature, matcherObj.part, requestConfig.interactSh)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
        if MatcherUtil.matchResultWithCondition(matcherResultList, requestConfig.matchersCondition):
            return True
        else:
            return False

    def fireRequestsAndAnalyzeResponse(self, dataReq, requestConfig, session=None):
        if dataReq["urlObj"].method.lower() == "get":
            try:
                response, position, id = RequestHandle.sendGetRequest(dataReq, requestConfig, session)
            except:
                response = None

            return {"response": response, "position": position, "id": id}
        elif dataReq["urlObj"].method.lower() == "post":
            try:
                response, position, id = RequestHandle.sendPostRequest(dataReq, requestConfig, session)
            except:
                response = None
            return {"response": response, "position": position, "id": id}


    def fireRequestWithCookieReuse(self, requestConfigObj, requestObjDict):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = True
        responseDataDictList = list()
        if requestConfigObj.payload:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.injectAllRawRequest(requestConfigObj, requestObjList)
                    for dataReq in dataReqList:
                        responseDataDictList.append(self.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session))
        else:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.getDataRequestWithoutPayloads(requestObjList)
                    for dataReq in dataReqList:
                        responseDataDictList.append(self.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session))
        self.analyzeResponse(responseDataDictList, requestConfigObj)

    def fireRequestWithMultiThread(self, requestConfigObj, requestObjDict):
        if requestConfigObj.payload:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.injectAllRawRequest(requestConfigObj, requestObjList)
                    responseDataDictList = self.runner(dataReqList, requestConfigObj)

        else:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.getDataRequestWithoutPayloads(requestObjList)
                    responseDataDictList = self.runner(dataReqList, requestConfigObj)
        self.analyzeResponse(responseDataDictList, requestConfigObj)

    def analyzeResponse(self, responseDataDictList, requestConfig):
        for responseDataDict in responseDataDictList:
            response = responseDataDict["response"]
            position = responseDataDict["position"]
            id = responseDataDict["id"]
            if response != None:
                resObj = ResponseGenerator.generateResponseObject(response, position, id)
                matcherResult = self.matcherProcess(resObj, requestConfig)
                print(resObj.id)
                print(matcherResult)
            else:
                print("Muc tieu khong phan hoi")

    def raccoonFlowControl(self, requestConfigObj, requestObjDict):
        PayloadInjection.injectInteractShUrl(requestConfigObj, requestObjDict)
        if requestConfigObj.cookieReuse:
            self.fireRequestWithCookieReuse(requestConfigObj, requestObjDict)
        else:
            self.fireRequestWithMultiThread(requestConfigObj, requestObjDict)
