import re

class ExposerUtil:
    @staticmethod
    def getRegexResultList(responseObject, exposerRegexList, part, interactsh):
        if responseObject and exposerRegexList and part:
            listResult = []
            data = ExposerUtil.getResponseByPart(responseObject, part, interactsh)
            if data:
                for regex in exposerRegexList:
                    if re.findall(regex, data):
                        listResult += re.findall(regex, data)
            return listResult
        else:
            return []

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