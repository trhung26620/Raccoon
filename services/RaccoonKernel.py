from concurrent.futures import ThreadPoolExecutor
from services.RequestHandle import RequestHandle
from services import PayloadInjection
from utils.ConfigUtil import ConfigUtil
from generator.ResponseGenerator import ResponseGenerator
from generator.TemplateConfigGenerator import TemplateConfigService
from utils.MatcherUtil import MatcherUtil
from config.StaticData import Template
from utils.ExposerUtil import ExposerUtil
from models.HTMLReport import HTMLReport
from config.StaticData import HTMLReportGlobal
import requests
from config.StaticData import Debug
from utils.PrinterUtil import Printer
from utils.TemplateUtil import TemplateUtil
from config.StaticData import SeverityCounter


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

    def matcherProcess(self, response, requestConfig, matcherObjList, dataList):
        matcherResultList = list()
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
        # print(matcherResultList)
        if MatcherUtil.matchResultWithCondition(matcherResultList, requestConfig.matchersCondition):
            return True
        else:
            return False

    def exposerProcess(self, response, requestConfig, exposerObjList, sshDataList):
        # exposerObjList = TemplateConfigService.generateExtractorObjectList(Template.templatePath)
        matcherResultList = list()
        if exposerObjList:
            for exposer in exposerObjList:
                if exposer.type == "xpath":
                    # result = ExposerUtil.getXpathResultList(response, exposer.signature, exposer.attribute, requestConfig.interactSh)
                    matcherResultList += ExposerUtil.getXpathResultList(response, exposer.signature, exposer.attribute, sshDataList)
                elif exposer.type == "regex":
                    matcherResultList += ExposerUtil.getRegexResultList(response, exposer.signature, exposer.part, sshDataList, exposer.group)
                elif exposer.type == "kval":
                    matcherResultList += ExposerUtil.getKeyValueResultList(response, exposer.signature, sshDataList)
            if matcherResultList:
                return matcherResultList
            else:
                return [None]
        else:
            return [None]


    def fireRequestsAndAnalyzeResponse(self, dataReq, requestConfig, session=None):
        if dataReq["urlObj"].method.lower() == "get":
            try:
                response, position, id, payloadInfo, url = RequestHandle.sendGetRequest(dataReq, requestConfig, session)
            except:
                response, position, id, payloadInfo, url = None, None, None, None, None
            return {"response": response, "position": position, "id": id, "payloadInfo": payloadInfo, "url": url}
        elif dataReq["urlObj"].method.lower() == "post":
            try:
                response, position, id, payloadInfo, url = RequestHandle.sendPostRequest(dataReq, requestConfig, session)
            except:
                response, position, id, payloadInfo, url = None, None, None, None, None
            return {"response": response, "position": position, "id": id, "payloadInfo": payloadInfo, "url": url}


    def fireRequestWithCookieReuse(self, requestConfigObj, requestObjDict):
        session = requests.Session()
        session.proxies.update(ConfigUtil.readConfig()["proxy"])
        session.verify = False
        session.allow_redirects = True
        responseDataDictList = list()
        isVerboseEnable = ConfigUtil.isVerboseEnable()

        if requestConfigObj.payload:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.injectAllRawRequest(requestConfigObj, requestObjList)
                    for dataReq in dataReqList:
                        responseDataDictList.append(self.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session))
                        for request, response in zip(requestObjList, responseDataDictList):
                            debugObject = {request: response}
                            Debug.DebugInfo.append(debugObject)
                            requestMethod = request.url.method
                            injectedUrl = response["url"]
                            if isVerboseEnable:
                                Printer.printInfo("Sending " + str(requestMethod) + " to: " + str(injectedUrl))
        else:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.getDataRequestWithoutPayloads(requestObjList)
                    for dataReq in dataReqList:
                        responseDataDictList.append(self.fireRequestsAndAnalyzeResponse(dataReq, requestConfigObj, session))
                        for request, response in zip(requestObjList, responseDataDictList):
                            debugObject = {request: response}
                            Debug.DebugInfo.append(debugObject)
                            requestMethod = request.url.method
                            injectedUrl = response["url"]
                            if isVerboseEnable:
                                Printer.printInfo("Sending " + str(requestMethod) + " to: " + str(injectedUrl))
        self.analyzeResponse(responseDataDictList, requestConfigObj)

    def fireRequestWithMultiThread(self, requestConfigObj, requestObjDict):

        isVerboseEnable = ConfigUtil.isVerboseEnable()

        if requestConfigObj.payload:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.injectAllRawRequest(requestConfigObj, requestObjList)
                    responseDataDictList = self.runner(dataReqList, requestConfigObj)
                    for request, response in zip(requestObjList, responseDataDictList):
                        debugObject = {request: response}
                        Debug.DebugInfo.append(debugObject)
                        requestMethod = request.url.method
                        injectedUrl = response["url"]
                        if isVerboseEnable:
                            Printer.printInfo("Sending " + str(requestMethod) + " to: " + str(injectedUrl))
                    self.analyzeResponse(responseDataDictList, requestConfigObj)
        else:
            for url, requestObjList in requestObjDict.items():
                if requestObjList:
                    dataReqList = PayloadInjection.getDataRequestWithoutPayloads(requestObjList)
                    responseDataDictList = self.runner(dataReqList, requestConfigObj)
                    for request, response in zip(requestObjList, responseDataDictList):
                        debugObject = {request: response}
                        Debug.DebugInfo.append(debugObject)
                        requestMethod = request.url.method
                        injectedUrl = response["url"]
                        if isVerboseEnable:
                            Printer.printInfo("Sending " + str(requestMethod) + " to: " + str(injectedUrl))
                    self.analyzeResponse(responseDataDictList, requestConfigObj)

    def analyzeResponse(self, responseDataDictList, requestConfig):
        matcherObjList = TemplateConfigService.generateMatcherObjectList(Template.templatePath, requestConfig.reqCondition)

        if not matcherObjList:
            return False
        dataList = None

        if requestConfig.interactSh:
            dataInteractsh, aes_key = requestConfig.interactSh.pollDataFromWeb()
            if aes_key:
                key = requestConfig.interactSh.decryptAESKey(aes_key)
                dataList = requestConfig.interactSh.decryptMessage(key, dataInteractsh)

        # get verbose value from config
        isVerboseEnable = ConfigUtil.isVerboseEnable()

        # List of HTML report object
        # HTMLReportList = []
        for responseDataDict in responseDataDictList:
            response = responseDataDict["response"]
            position = responseDataDict["position"]
            id = responseDataDict["id"]
            payloadInfo = responseDataDict["payloadInfo"]
            injectedUrl = responseDataDict["url"]
            if response is not None:
                resObj = ResponseGenerator.generateResponseObject(response, position, id, payloadInfo)
                matcherResult = self.matcherProcess(resObj, requestConfig, matcherObjList, dataList)
                currentUsedTemplatePath = Template.templatePath
                if matcherResult:
                    Printer.printScanResult(injectedUrl, "Payload: " + str(payloadInfo), matcherResult, currentUsedTemplatePath)
                else:
                    if isVerboseEnable:     # verbose to print all result (event not infected)
                        Printer.printScanResult(injectedUrl, "Target is negative", matcherResult, currentUsedTemplatePath)
                exposerObjList = TemplateConfigService.generateExtractorObjectList(Template.templatePath)
                if matcherResult:
                    info = self.exposerProcess(resObj, requestConfig, exposerObjList, dataList)

                    # find severity of current template
                    severity = str(TemplateUtil.getTemplateSeverity(Template.templatePath)).lower()
                    if severity is not None:
                        currentPayload = Template.templatePath
                        if currentPayload not in SeverityCounter.vulnerableTemplates:
                            SeverityCounter.vulnerableTemplates.append(currentPayload)
                            if severity == "info":
                                SeverityCounter.infoSeverityCounter += 1
                            elif severity == "low":
                                SeverityCounter.lowSeverityCounter += 1
                            elif severity == "medium":
                                SeverityCounter.mediumSeverityCounter += 1
                            elif severity == "high" or severity == "critical":
                                SeverityCounter.highSeverityCounter += 1

                    # Default value if exposer and payload dict is none
                    if None in info and len(info) == 1:
                        info = []
                    if payloadInfo is None:
                        payloadInfo = {}
                    HTMLReportObject = HTMLReport(injectedUrl, Template.templatePath, info, payloadInfo)  # payload here is dict
                    HTMLReportGlobal.HTMLReportList.append(HTMLReportObject)
                    if requestConfig.stopAtFirstMatch:
                        break
            else:
                if isVerboseEnable:
                    Printer.printError("No response from target: " + injectedUrl)


    def raccoonFlowControl(self, requestConfigObj, requestObjDict):
        PayloadInjection.injectInteractShUrl(requestConfigObj, requestObjDict)
        if requestConfigObj.cookieReuse:
            self.fireRequestWithCookieReuse(requestConfigObj, requestObjDict)
        else:
            self.fireRequestWithMultiThread(requestConfigObj, requestObjDict)
