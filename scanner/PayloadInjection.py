import itertools
from utils.ExtendedUtil import ExtendedUtil
from config.StaticData import Parttern
import copy

def batteringramModeInjection(payloadDict, dataDict):
        if len(payloadDict) != 1:
            print("Using batteringram mode is given only one payload list.")
            exit()
        payloadName = ExtendedUtil.getListKeyFromDict(payloadDict)[0]
        for payload in payloadDict[payloadName]:
            dataList = []
            for key, data in dataDict.items():
                if isinstance(data, dict):
                    if not data:
                        dataList.append(None)
                    else:
                        tempDict = copy.deepcopy(data)
                        dataList.append(ExtendedUtil.findAndReplaceInDict(tempDict, '{{' + payloadName + '}}', payload))
                elif isinstance(data, str):
                    if not data:
                        dataList.append(None)
                    else:
                        dataList.append(data.replace('{{' + payloadName + '}}', payload))
                else:
                    dataList.append(None)
            yield {"requestData": dataList, "payloadInfo": {payloadName: payload}}


def pitchforkModeInjection(payloadDict, dataDict):
    payloadNameList = ExtendedUtil.getListKeyFromDict(payloadDict)
    smallestSize = len(payloadDict[payloadNameList[0]])
    for k,v in payloadDict.items():
        if smallestSize > len(v):
            smallestSize = len(v)
    for i in range(smallestSize):
        dataList = []
        payloadInfo = dict()
        for key, data in dataDict.items():
            if isinstance(data, dict):
                if not data:
                    dataList.append(None)
                else:
                    tempDict = copy.deepcopy(data)
                    for payloadName in payloadNameList:
                        tempDict = ExtendedUtil.findAndReplaceInDict(tempDict, "{{" + payloadName + "}}", payloadDict[payloadName][i])
                    dataList.append(tempDict)
            elif isinstance(data, str):
                if not data:
                    dataList.append(None)
                else:
                    tempString = data
                    for payloadName in payloadNameList:
                        tempString = tempString.replace('{{' + payloadName + '}}', payloadDict[payloadName][i])
                    dataList.append(tempString)
        for payloadName in payloadNameList:
            payloadInfo[payloadName] = payloadDict[payloadName][i]
        yield {"requestData": dataList, "payloadInfo": payloadInfo}

def clusterbombModeInjection(payloadDict, dataDict):
    payloadNameList = ExtendedUtil.getListKeyFromDict(payloadDict)
    bigPayloadList = []
    for payloadName in payloadNameList:
        bigPayloadList.append(payloadDict[payloadName])
    payloadTupleList = list(itertools.product(*bigPayloadList))
    for payloadTuple in payloadTupleList:
        dataList = []
        payloadInfo = dict()
        for key, data in dataDict.items():
            if isinstance(data, dict):
                if not data:
                    dataList.append(None)
                else:
                    tempDict = copy.deepcopy(data)
                    for i in range(len(payloadNameList)):
                        tempDict = ExtendedUtil.findAndReplaceInDict(tempDict, "{{" + payloadNameList[i] + "}}", payloadTuple[i])
                    dataList.append(tempDict)
            elif isinstance(data, str):
                if not data:
                    dataList.append(None)
                else:
                    tempString = data
                    for i in range(len(payloadNameList)):
                        tempString = tempString.replace('{{' + payloadNameList[i] + '}}', payloadTuple[i])
                    dataList.append(tempString)
        for i in range(len(payloadNameList)):
            payloadInfo[payloadNameList[i]] = payloadTuple[i]
        yield {"requestData": dataList, "payloadInfo": payloadInfo}


def injectInteractShUrl(requestConfigObj, requestObjDict):
    parttern = Parttern.interactUrl
    if requestConfigObj.interactShUrl:
        for url, reqObjList in requestObjDict.items():
            for reqObj in reqObjList:
                if reqObj.header.content:
                    reqObj.header.content = ExtendedUtil.findAndReplaceInDict(reqObj.header.content, parttern, requestConfigObj.interactShUrl)
                if reqObj.body.content:
                    reqObj.body.content = reqObj.body.content.replace(parttern, requestConfigObj.interactShUrl)
                if reqObj.url.host:
                    reqObj.url.host = reqObj.url.host.replace(parttern, requestConfigObj.interactShUrl)
                if reqObj.url.path:
                    reqObj.url.path = reqObj.url.path.replace(parttern, requestConfigObj.interactShUrl)
                if reqObj.url.paramPath:
                    reqObj.url.paramPath = ExtendedUtil.findAndReplaceInDict(reqObj.url.paramPath, parttern, requestConfigObj.interactShUrl)
                if reqObj.url.baseUrl:
                    reqObj.url.baseUrl = reqObj.url.baseUrl.replace(parttern, requestConfigObj.interactShUrl)

def injectAllRawRequest(requestsConfig, requestObjList):
    for request in requestObjList:
        scanMode = requestsConfig.scanMode
        dataDict = {
            "header_content": request.header.content,
            "url_path_param": request.url.paramPath,
            "body_content": request.body.content
        }
        requestInfoList = None
        if scanMode == "batteringram":
            requestInfoList = batteringramModeInjection(requestsConfig.payload.payloadValue, dataDict)

        elif scanMode == "pitchfork":
            requestInfoList = pitchforkModeInjection(requestsConfig.payload.payloadValue, dataDict)

        elif scanMode == "clusterbomb":
            requestInfoList = clusterbombModeInjection(requestsConfig.payload.payloadValue, dataDict)

        id = 1
        for requestInfo in requestInfoList:
            requestData = requestInfo["requestData"]
            payloadInfo = requestInfo["payloadInfo"]
            yield {"header": requestData[0], "param": requestData[1], "body": requestData[2], "urlObj": request.url,
                   "position": request.position, "id": id,
                   "payloadInfo": payloadInfo}
            id += 1

def getDataRequestWithoutPayloads(requestObjList):
    id = 1
    for request in requestObjList:
        yield {"header": request.header.content, "param": request.url.paramPath, "body": request.body.content, "urlObj": request.url, "position": request.position, "id": id, "payloadInfo": None}
        id +=1


