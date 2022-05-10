import re
from bs4 import BeautifulSoup

class ExposerUtil:
    @staticmethod
    def getRegexResultList(responseObject, exposerRegexList, part, interactsh, group):
        if responseObject and exposerRegexList and part:
            listResult = []
            data = ExposerUtil.getResponseByPart(responseObject, part, interactsh)
            if data:
                for regex in exposerRegexList:
                    if re.findall(regex, data):
                        listResult += re.findall(regex, data)
            if group > len(listResult) or group < 0:
                return listResult
            elif group != 0:
                return listResult[group-1]
            else:
                return listResult
        else:
            return None

    @staticmethod
    def getXpathResultList(responseObject, xpathRegexList, attribute,interactsh):
        if responseObject and xpathRegexList:
            listResult = []
            data = ExposerUtil.getResponseByPart(responseObject, "body", interactsh)
            if data:
                for xpath in xpathRegexList:
                    tagData = ExposerUtil.getDataFromXpath(data, xpath, attribute)
                    listResult.append(tagData)
                if listResult:
                    return listResult
                else:
                    return None
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
                        data = ExposerUtil.concatProtocolInteractsh(dataList)
                    elif "interactsh_request" in part:
                        data = ExposerUtil.concatRequestInteractsh(dataList)
                    elif "interactsh_response" in part:
                        data = ExposerUtil.concatResponseInteractsh(dataList)
                else:
                    return None
            return data
        else:
            return None

    @staticmethod
    def getSubTagIndex(tag):
        subTag = None
        subTagList = re.findall("[a-zA-Z0-9]+\[.+[\]]$",tag)
        if subTagList:
            subTag = subTagList[0]
        if subTag:
            if "@id=" in subTag:
                id = subTag.split("@id=")[1].strip().split("]")[0].strip()[1:-1]
                return {"id": id}
            elif "@class=" in subTag:
                className = subTag.split("@class=")[1].strip().split("]")[0].strip()[1:-1]
                return {"className": className}
            try:
                index = subTag.split("[")[1].split("]")[0]
                if index:
                    index = int(index)
                    if index > 0:
                        return {"index": index}
                    else:
                        return None
            except:
                return None
        return None

    @staticmethod
    def getDataFromXpath(data, xpath, attribute):
        result = ""
        index = 0
        tagList = xpath.split("/")[1:]
        soup = BeautifulSoup(data, 'html.parser')
        count = 0
        for tag in tagList:
            count += 1
            subTagIndex = ExposerUtil.getSubTagIndex(tag)
            if not subTagIndex:
                resultList = soup.find_all(tag)
            elif "id" in subTagIndex:
                tag = tag.split("[")[0].strip()
                resultList = soup.find_all(tag, id=subTagIndex["id"])
            elif "className" in subTagIndex:
                tag = tag.split("[")[0].strip()
                resultList = soup.find_all(tag, {"class": subTagIndex["className"]})
            elif "index" in subTagIndex:
                tag = tag.split("[")[0].strip()
                if subTagIndex["index"] <= len(soup.find_all(tag)):
                    index = subTagIndex["index"] - 1
                    resultList = soup.find_all(tag)
                else:
                    return None
            else:
                return None
            if resultList:
                if count == len(tagList):
                    if attribute:
                        result = resultList[index].get(attribute)
                    else:
                        result = resultList[index].get_text()
                        if not result:
                            result = None
                else:
                    result = str(resultList[index])
                    soup = BeautifulSoup(result, 'html.parser')
                    index = 0
            else:
                return None
        return result