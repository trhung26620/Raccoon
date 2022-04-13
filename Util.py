def findAndReplaceInDict(rawDict, findStr, replaceStr):
    if isinstance(rawDict, dict):
        for k, v in rawDict.items():
            if v.find(findStr) > -1:
                rawDict[k] = v.replace(findStr, replaceStr)
        return rawDict
    else:
        print("rawDict must be a dict type")
        exit

def getListKeyFromDict(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list
