import re

class MatcherUtil:
    @staticmethod
    def statusMatchResultList(responseStatus, matcherStatusList):
        if responseStatus and matcherStatusList:
            listResult = list()
            for matcherStatus in matcherStatusList:
                if int(matcherStatus)==int(responseStatus):
                    listResult.append(True)
                else:
                    listResult.append(False)
            return listResult
        else:
            return None

    @staticmethod
    def timeMatchResultList(responseTime, matcherTimeList):
        if responseTime and matcherTimeList:
            listResult = list()
            for matcherTime in matcherTimeList:
                listResult.append(MatcherUtil.compareTimeMatcherData(responseTime, matcherTime))
            return listResult
        else:
            return None

    @staticmethod
    def wordMatchResultList(responseObject, matcherWordList, part, interactshDataList):
        if responseObject and matcherWordList and part:
            listResult = list()
            data = MatcherUtil.getResponseByPart(responseObject, part, interactshDataList)
            if data:
                for word in matcherWordList:
                    if word in data:
                        listResult.append(True)
                    else:
                        listResult.append(False)
            else:
                listResult.append(False)
            return listResult

        else:
            return None

    @staticmethod
    def regexMatchResultList(responseObject, matcherRegexList, part, interactshDataList):
        if responseObject and matcherRegexList and part:
            listResult = list()
            data = MatcherUtil.getResponseByPart(responseObject, part, interactshDataList)
            if data:
                for regex in matcherRegexList:
                    if re.search(regex, data):
                        listResult.append(True)
                    else:
                        listResult.append(False)
            else:
                listResult.append(False)
            return listResult
        else:
            return None

    @staticmethod
    def concatProtocolInteractsh(dataInteractsh):
        if dataInteractsh:
            protocols = ""
            for data in dataInteractsh:
                protocols += data["protocol"] + "\n"
            return protocols[:-1]
        else:
            return None

    @staticmethod
    def concatRequestInteractsh(dataInteractsh):
        if dataInteractsh:
            requestRaws = ""
            for data in dataInteractsh:
                requestRaws += data["raw-request"] + "\n"
            return requestRaws[:-1]
        else:
            return None

    @staticmethod
    def concatResponseInteractsh(dataInteractsh):
        if dataInteractsh:
            responseRaws = ""
            for data in dataInteractsh:
                responseRaws += data["raw-response"] + "\n"
            return responseRaws[:-1]
        else:
            return None

    @staticmethod
    def getResponseByPart(responseObject, part, interactshDataList):
        if responseObject and part:
            data = ""
            if "header" in part:
                data = responseObject.header
            elif "body" in part:
                data = responseObject.body
            elif "all" in part:
                data =responseObject.headerAndBody
            elif "interactsh_protocol" in part or "interactsh_request" in part or "interactsh_response" in part:
                if interactshDataList:
                    if "interactsh_protocol" in part:
                        data = MatcherUtil.concatProtocolInteractsh(interactshDataList)
                    elif "interactsh_request" in part:
                        data = MatcherUtil.concatRequestInteractsh(interactshDataList)
                    elif "interactsh_response" in part:
                        data = MatcherUtil.concatResponseInteractsh(interactshDataList)
                else:
                    return None
            return data
        else:
            return None


    @staticmethod
    def matchResultWithCondition(matchResultList, condition):
        if matchResultList:
            if condition == "or":
                for matchResult in matchResultList:
                    if matchResult == True:
                        return True
                return False
            elif condition == "and":
                for matchResult in matchResultList:
                    if matchResult == False:
                        return False
                return True
        else:
            return None

    @staticmethod
    def finalMatchResult(matchResultList, condition, negative):
        result = MatcherUtil.matchResultWithCondition(matchResultList, condition)
        if result == True or result == False:
            if negative:
                return not result
            elif not negative:
                return result
        else:
            return None

    @staticmethod
    def compareTimeMatcherData(responseTime, timeMatcherString):
        if ">=" in timeMatcherString:
            if float(responseTime) >= float(timeMatcherString.split(">=")[1].strip()):
                return True
            else:
                return False
        elif "<=" in timeMatcherString:
            if float(responseTime) <= float(timeMatcherString.split("<=")[1].strip()):
                return True
            else:
                return False
        elif ">" in timeMatcherString:
            if float(responseTime) > float(timeMatcherString.split(">")[1].strip()):
                return True
            else:
                return False
        elif "<" in timeMatcherString:
            if float(responseTime) < float(timeMatcherString.split("<")[1].strip()):
                return True
            else:
                return False
        else:
            return None

