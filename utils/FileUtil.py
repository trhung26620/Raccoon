import os

class FileUtil:
    @staticmethod
    def readPayloadFromFile(filePath):
        try:
            isFileExist = os.path.isfile(filePath)
            payloadValues = []
            # print(isFileExist)
            # exit()
            if isFileExist:
                fileObject = open(filePath, "r")
                for payloadValue in fileObject:
                    payloadValue = payloadValue.strip()
                    if payloadValue.strip():
                        payloadValues.append(payloadValue)
                return payloadValues
            else:
                print("File not found !!!")
                return None
        except FileNotFoundError:
            print("Can not read this file !!! ")
            fileObject.close()
            return None



