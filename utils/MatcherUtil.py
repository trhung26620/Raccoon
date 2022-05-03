import re
import base64
import html
from urllib.parse import quote as url_encode, unquote as url_decode

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
    def wordMatchResultList(responseObject, matcherWordList, part, interactsh):
        if responseObject and matcherWordList and part:
            listResult = list()
            data = MatcherUtil.getResponseByPart(responseObject, part, interactsh)
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
    def regexMatchResultList(responseObject, matcherRegexList, part, interactsh):
        if responseObject and matcherRegexList and part:
            listResult = list()
            data = MatcherUtil.getResponseByPart(responseObject, part, interactsh)
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
    def getResponseByPart(responseObject, part, interactsh):
        if responseObject and part:
            data = ""
            if "header" in part:
                data = responseObject.header
            elif "body" in part:
                data = responseObject.body
            elif "all" in part:
                data =responseObject.headerAndBody
            elif "interactsh_protocol" in part or "interactsh_request" in part or "interactsh_response" in part:
                if interactsh:
                    dataList = None
                    dataInteractsh, aes_key = interactsh.pollDataFromWeb()
                    if aes_key:
                        key = interactsh.decryptAESKey(aes_key)
                        dataList = interactsh.decryptMessage(key, dataInteractsh)
                    if "interactsh_protocol" in part:
                        data = MatcherUtil.concatProtocolInteractsh(dataList)
                    elif "interactsh_request" in part:
                        data = MatcherUtil.concatRequestInteractsh(dataList)
                    elif "interactsh_response" in part:
                        data = MatcherUtil.concatResponseInteractsh(dataList)
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

class Helper:
    @staticmethod
    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    @staticmethod
    def remove_suffix(text, suffix):
        if text.endswith(suffix):
            return text[:-len(suffix)]
        return text

#eval("base64.b64encode(data)")
# message = "Python is fun"
# data = eval("""base64.b64encode(message.encode('ascii')).decode('ascii')""")
# https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
arg1 = r"""https://projectdiscovery.io/test?a=1"""
# arg1 = input()
arg2 = r"aa"
arg3 = r""
helperDict = {
    "base64": "(base64.b64encode(arg1.encode('ascii')).decode('ascii'))",
    "base64_decode": """(base64.b64decode(arg1.encode("ascii")).decode("ascii"))""",
    "concat": "(arg1 + arg2)",
    "contains": "(arg2 in arg1)",
    "html_escape": "(html.escape(arg1))",
    "html_unescape": "(html.unescape(arg1))",
    "len": "(len(arg1))",
    "regex": "(bool(re.match(arg1,arg2)))",
    "repeat": "(arg1*int(arg2))",
    "replace": "(arg1.replace(arg2,arg3))",
    "replace_regex": "(re.sub(arg2, arg3, arg1))",
    "to_lower": "(arg1.lower())",
    "to_upper": "(arg1.upper())",
    "trim": "(arg1.strip(arg2))",
    "trim_left": "(arg1.lstrip(arg2))",
    "trim_righ": "(arg1.rstrip(arg2))",
    "trim_prefix": "(Helper.remove_prefix(arg1,arg2))",
    "trim_space": """(arg1.strip(" "))""",
    "trim_suffix": "(Helper.remove_suffix(arg1,arg2))",
    "url_encode": "(url_encode(arg1, safe=''))",
    "url_decode": "(url_decode(arg1))"
}

def findManyIndex(data, pattern):
    return [i for i, ltr in enumerate(data) if ltr == pattern]

def checkValidParenthesis(helperString):
    openParenthesisIndexList = findManyIndex(helperString, "(")
    closeParenthesisIndexList = findManyIndex(helperString, ")")
    if not len(openParenthesisIndexList) == len(closeParenthesisIndexList):
        print("Error: Wrong helper systax")
        exit()

def getFunctionListWithName(functionName, helperString):
    functionPattern = functionName+"("
    resultList = []
    pos = 0
    while pos < len(helperString)-1:
        funcStartPosition = helperString.find(functionPattern, pos)
        if funcStartPosition != -1:
            argStartPosition = funcStartPosition + len(functionPattern)
            tempString = helperString[argStartPosition:]
            countOpenParenthesis = 0
            countChar = 0
            for char in tempString:
                countChar += 1
                if char == "(":
                    countOpenParenthesis +=1
                elif char == ")" and countOpenParenthesis == 0:
                    resultList.append(helperString[funcStartPosition:argStartPosition+countChar])
                    pos = funcStartPosition + len(helperString[funcStartPosition:argStartPosition+countChar])
                    print(pos)
                    break
                elif char == ")":
                    countOpenParenthesis -= 1
        else:
            break
    if resultList:
        return resultList
    else:
        return None

# """replace("abc,dxy",",d","xxx")"""
# # abcxxxxy
# # exit()
# functionList = ["contains", "to_lower"]
# data = """!contains(to_lower(body), to_lower("<HTML"))"""
# data1 = """(!contains(body_1, "It works")) && (contains(body_2, "It works") || contains(body_3, "It works")) || contains(body_4, "It works") || contains(body_5, "It works") || contains(body_6, "It works") || contains(body_7, "It works") || contains(body_8, "It works") || contains(body_9, "It works") || contains(body_10, "It works") || contains(body_11, "It works") || contains(body_12, "It works") || contains(body_13, "It works") || contains(body_14, "It works") || contains(body_15, "It works") || contains(body_16, "It works") || contains(body_17, "It works") || contains(body_18, "It works") || contains(body_19, "It works") || contains(body_20, "It works") || contains(body_21, "It works") || contains(body_22, "It works") || contains(body_23, "It works")"""
#
# checkValidParenthesis(data1)
# result = getFunctionListWithName("to_lower", data)
# print(result)







# for function in functionList:
#     if data.find(function):
#         tempPos = data.find(function)+len(function)
#         print(tempPos)
#         print(data[tempPos])
#     print("+"*50)

# print("(")
# print(data.find("contains("))
# print(find(data,"contains"))

# print(")")
# print(find(data,")"))
