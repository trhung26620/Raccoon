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

    def matcherProcess(self, response, requestConfig):
        matcherObjList = TemplateConfigService.generateMatcherObjectList(Template.templatePath, requestConfig.reqCondition)
        matcherResultList = list()
        dataList = None
        if requestConfig.interactSh:
            dataInteractsh, aes_key = requestConfig.interactSh.pollDataFromWeb()
            if aes_key:
                key = requestConfig.interactSh.decryptAESKey(aes_key)
                dataList = requestConfig.interactSh.decryptMessage(key, dataInteractsh)
        defaultPart = ["header", "body", "all", "interactsh_protocol", "interactsh_request", "interactsh_response"]
        for matcherObj in matcherObjList:
            if matcherObj.part:
                if matcherObj.part in defaultPart or str(response.position) == matcherObj.part.split("_")[1]:
                    if matcherObj.type == "status":
                        result = MatcherUtil.statusMatchResultList(response.status, matcherObj.signature)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
                    elif matcherObj.type == "word":
                        result = MatcherUtil.wordMatchResultList(response, matcherObj.signature, matcherObj.part, dataList)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
                    elif matcherObj.type == "time":
                        result = MatcherUtil.timeMatchResultList(response.time, matcherObj.signature)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
                    elif matcherObj.type == "regex":
                        result = MatcherUtil.regexMatchResultList(response, matcherObj.signature, matcherObj.part, dataList)
                        result = MatcherUtil.finalMatchResult(result, matcherObj.condition, matcherObj.negative)
                        matcherResultList.append(result)
        if MatcherUtil.matchResultWithCondition(matcherResultList, requestConfig.matchersCondition):
            return True
        else:
            return False

    def fireRequestsAndAnalyzeResponse(self, dataReq, requestConfig, session=None):
        if dataReq["urlObj"].method.lower() == "get":
            try:
                response, position = RequestHandle.sendGetRequest(dataReq, requestConfig, session)
            except:
                response = None
            if response != None:
                resObj = ResponseGenerator.generateResponseObject(response, position)
                matcherResult = self.matcherProcess(resObj, requestConfig)
                print(matcherResult)
            else:
                print("Muc tieu khong phan hoi")
        elif dataReq["urlObj"].method.lower() == "post":
            try:
                response, position = RequestHandle.sendPostRequest(dataReq, requestConfig, session)
            except:
                response = None
            if response != None:
                resObj = ResponseGenerator.generateResponseObject(response, position)
                matcherResult = self.matcherProcess(resObj, requestConfig)
                print(matcherResult)
            else:
                print("Muc tieu khong phan hoi")

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

    def raccoonFlowControl(self, requestConfigObj, requestObjDict):
        PayloadInjection.injectInteractShUrl(requestConfigObj, requestObjDict)
        if requestConfigObj.cookieReuse:
            self.fireRequestWithCookieReuse(requestConfigObj, requestObjDict)
        else:
            self.fireRequestWithMultiThread(requestConfigObj, requestObjDict)