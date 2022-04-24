import itertools
from concurrent.futures import ThreadPoolExecutor
from scanner.RequestHandle import RequestHandle
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

def injectAllRawRequest(requestConfig, request):
    scanMode = requestConfig.scanMode
    if scanMode == "batteringram":
        headerList = batteringramModeDictInjection(requestConfig.payload.payloadVal, request.header.content)
        paramList = batteringramModeDictInjection(requestConfig.payload.payloadVal, request.url.param)
        bodyList = batteringramModeStringInjection(requestConfig.payload.payloadVal, request.body.content)
        for header, param, body in zip(headerList, paramList, bodyList):
            yield {"header": header, "param": param, "body": body}
    elif scanMode == "pitchfork":
        headerList = pitchforkModeDictInjection(requestConfig.payload.payloadVal, request.header.content)
        paramList = pitchforkModeDictInjection(requestConfig.payload.payloadVal, request.url.param)
        bodyList = pitchforkModeStringInjection(requestConfig.payload.payloadVal, request.body.content)
        for header, param, body in zip(headerList, paramList, bodyList):
            yield {"header": header, "param": param, "body": body}
    elif scanMode == "pitchfork":
        headerList = clusterbombModeDictInjection(requestConfig.payload.payloadVal, request.header.content)
        paramList = clusterbombModeDictInjection(requestConfig.payload.payloadVal, request.url.param)
        bodyList = clusterbombModeStringInjection(requestConfig.payload.payloadVal, request.body.content)
        for header, param, body in zip(headerList, paramList, bodyList):
            yield {"header": header, "param": param, "body": body}

def runner(dataReqList, requestConfig, request):
    threads= []
    with ThreadPoolExecutor(max_workers=requestConfig.thread) as executor:
        if request.url.method.lower() == "get":
            for dataReq in dataReqList:
                threads.append(executor.submit(RequestHandle.sendGetRequest, request.url.path, dataReq["param"], dataReq["header"], dataReq["body"], requestConfig.HTTP_PROXY))
        elif request.url.method.lower() == "post":
            for dataReq in dataReqList:
                threads.append(executor.submit(RequestHandle.sendPostRequest, request.url.path, dataReq["param"], dataReq["header"], dataReq["body"], requestConfig.HTTP_PROXY))

def fireRequests(requestConfig, request):
    dataReqList = injectAllRawRequest(requestConfig, request)
    runner(dataReqList, requestConfig, request)

