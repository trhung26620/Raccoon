import os


class FileUtil:

    @staticmethod
    def readPayloadFromFile(filePath):
        try:
            isFileExist = os.path.isfile(filePath)
            payloadValues = []
            if isFileExist:
                fileObject = open(filePath, "r")
                for payloadValue in fileObject:
                    payloadValue = payloadValue.strip()
                    if payloadValue.strip():
                        # print(" [FileUtils] - Read line: " + payloadValue)
                        payloadValues.append(payloadValue)
                    fileObject.close()
                    # print("List payload: " + str(payloadValues))
            else:
                print("File not found !!!!")
        except FileNotFoundError:
            print("File exception !!! ")

