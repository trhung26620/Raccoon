from models.InteractShData import InteractShData

class InteractshGenerator:
    @staticmethod
    def generateInteractDataObjList(interact):
        if interact:
            data, aes_key = interact.pollDataFromWeb()
            if aes_key:
                key = interact.decryptAESKey(aes_key)
                dataList = interact.decryptMessage(key, data)
                if dataList:
                    interactDataObjList = list()
                    for data in dataList:
                        protocol = data["protocol"]
                        request = data["raw-request"]
                        response = data["raw-response"]
                        interactData = InteractShData(protocol, request, response)
                        interactDataObjList.append(interactData)
                    return interactDataObjList
                else:
                    return None
            else:
                print("Error occurred with interactsh server")
                return None
        else:
            print("Error occurred with interactsh server")
            return None

