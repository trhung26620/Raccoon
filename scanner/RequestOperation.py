import itertools
from utils.ExtendedUtil import ExtendedUtil
# import Util

def batteringramModeDictInjection(payloadDict, dataDict):
    if len(payloadDict) != 1:
        print("Using batteringram mode is given only one payload list.")
        exit()
    payloadName = ExtendedUtil.getListKeyFromDict(payloadDict)[0]
    for payload in payloadDict[payloadName]:
        if not dataDict:
            yield None
        else:
            tempDict = dataDict.copy()
            yield ExtendedUtil.findAndReplaceInDict(tempDict, '{{' + payloadName + '}}', payload)

def batteringramModeStringInjection(payloadDict, rawString):
    if len(payloadDict) != 1:
        print("Using batteringram mode is given only one payload list.")
        exit()
    payloadName = ExtendedUtil.getListKeyFromDict(payloadDict)[0]
    for payload in payloadDict[payloadName]:
        if not rawString:
            yield None
        else:
            yield rawString.replace('{{' + payloadName + '}}', payload)

def pitchforkModeDictInjection(payloadDict, dataDict):
    payloadNameList = ExtendedUtil.getListKeyFromDict(payloadDict)
    smallestSize = len(payloadDict[payloadNameList[0]])
    for k,v in payloadDict.items():
        if smallestSize > len(v):
            smallestSize = len(v)
    for i in range(smallestSize):
        if not dataDict:
            yield None
        else:
            tempDict = dataDict.copy()
            for payloadName in payloadNameList:
                tempDict = ExtendedUtil.findAndReplaceInDict(tempDict, "{{" + payloadName + "}}", payloadDict[payloadName][i])
            yield tempDict

def pitchforkModeStringInjection(payloadDict, rawString):
    payloadNameList = ExtendedUtil.getListKeyFromDict(payloadDict)
    smallestSize = len(payloadDict[payloadNameList[0]])
    for k,v in payloadDict.items():
        if smallestSize > len(v):
            smallestSize = len(v)
    for i in range(smallestSize):
        if not rawString:
            yield None
        else:
            tempString = rawString
            for payloadName in payloadNameList:
                tempString = tempString.replace('{{' + payloadName + '}}', payloadDict[payloadName][i])
            yield tempString

def clusterbombModeDictInjection(payloadDict, dataDict):
    payloadNameList = ExtendedUtil.getListKeyFromDict(payloadDict)
    bigPayloadList = []
    for payloadName in payloadNameList:
        bigPayloadList.append(payloadDict[payloadName])
    payloadTupleList = list(itertools.product(*bigPayloadList))
    for payloadTuple in payloadTupleList:
        if not dataDict:
            yield None
        else:
            tempDict = dataDict.copy()
            for i in range(len(payloadNameList)):
                tempDict = ExtendedUtil.findAndReplaceInDict(tempDict, "{{" + payloadNameList[i] + "}}", payloadTuple[i])
            yield tempDict

def clusterbombModeStringInjection(payloadDict, rawString):
    payloadNameList = ExtendedUtil.getListKeyFromDict(payloadDict)
    bigPayloadList = []
    for payloadName in payloadNameList:
        bigPayloadList.append(payloadDict[payloadName])
    payloadTupleList = list(itertools.product(*bigPayloadList))
    for payloadTuple in payloadTupleList:
        if not rawString:
            yield None
        else:
            tempString = rawString
            for i in range(len(payloadNameList)):
                tempString = tempString.replace('{{' + payloadNameList[i] + '}}', payloadTuple[i])
            yield tempString

def injectAllRawRequest(requestsConfig, requestObjList):
    for request in requestObjList:
        scanMode = requestsConfig.scanMode
        if scanMode == "batteringram":
            headerList = batteringramModeDictInjection(requestsConfig.payload.payloadValue, request.header.content)
            paramList = batteringramModeDictInjection(requestsConfig.payload.payloadValue, request.url.paramPath)
            bodyList = batteringramModeStringInjection(requestsConfig.payload.payloadValue, request.body.content)
            for header, param, body in zip(headerList, paramList, bodyList):
                yield {"header": header, "param": param, "body": body, "urlObj": request.url}

        elif scanMode == "pitchfork":
            headerList = pitchforkModeDictInjection(requestsConfig.payload.payloadValue, request.header.content)
            paramList = pitchforkModeDictInjection(requestsConfig.payload.payloadValue, request.url.paramPath)
            bodyList = pitchforkModeStringInjection(requestsConfig.payload.payloadValue, request.body.content)
            for header, param, body in zip(headerList, paramList, bodyList):
                yield {"header": header, "param": param, "body": body, "urlObj": request.url}

        elif scanMode == "clusterbomb":
            headerList = clusterbombModeDictInjection(requestsConfig.payload.payloadValue, request.header.content)
            paramList = clusterbombModeDictInjection(requestsConfig.payload.payloadValue, request.url.paramPath)
            bodyList = clusterbombModeStringInjection(requestsConfig.payload.payloadValue, request.body.content)
            for header, param, body in zip(headerList, paramList, bodyList):
                yield {"header": header, "param": param, "body": body, "urlObj": request.url}

def getDataRequestWithoutPayloads(requestObjList):
    for request in requestObjList:
        yield {"header": request.header.content, "param": request.url.paramPath, "body": request.body.content, "urlObj": request.url}


