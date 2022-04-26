class ExtendedUtil:
    @staticmethod
    def findAndReplaceInDict(rawDict, findStr, replaceStr):
        if isinstance(rawDict, dict):
            for k, v in rawDict.items():
                if isinstance(v, list):
                    for i in range(len(v)):
                        rawDict[k][i] = rawDict[k][i].replace(findStr, replaceStr)
                elif isinstance(v, str):
                    if v.find(findStr) > -1:
                        rawDict[k] = v.replace(findStr, replaceStr)
            return rawDict
        else:
            print("rawDict must be a dict type")
            exit

    @staticmethod
    def getListKeyFromDict(dict):
        list = []
        for key in dict.keys():
            list.append(key)
        return list
