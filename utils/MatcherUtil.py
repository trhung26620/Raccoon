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
    def wordMatchResultList(responseObject, matcherWordList, part):
        if responseObject and matcherWordList and part:
            listResult = list()
            data = MatcherUtil.getResponseByPart(responseObject, part)
            for word in matcherWordList:
                if word in data:
                    listResult.append(True)
                else:
                    listResult.append(False)
            return listResult
        else:
            return None

    @staticmethod
    def getResponseByPart(responseObject, part):
        if responseObject and part:
            data = ""
            if part == "header":
                data = responseObject.header
            elif part == "body":
                data = responseObject.body
            elif part == "all":
                data =responseObject.headerAndBody
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
