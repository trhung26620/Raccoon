from termcolor import colored
from datetime import datetime
import validators

class Printer:

    @staticmethod
    def printError(err):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        errorTag = colored("[ERROR]", "red", attrs=["bold"])
        print("[" + nowTag + "] " + errorTag + " " + str(err))


    @staticmethod
    def printWarning(warning):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        warningTag = colored("[WARNING]", "yellow", attrs=["underline"])
        print("[" + nowTag + "] " + warningTag + " " + str(warning))


    @staticmethod
    def printInfo(info):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        infoTag = colored("[INFO]", "blue", attrs=["underline"])
        print("[" + nowTag + "] " + infoTag + " " + str(info))

    @staticmethod
    def printScanResult(targetUrl, info, result, templatePath):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        targetUrlTag = colored(str(targetUrl), "blue")
        if result:
            infoTag = colored(info, "red")
        else:
            infoTag = colored(info, "green")

        if str(templatePath).strip() != '':
            from utils.TemplateUtil import TemplateUtil
            templateInfo = TemplateUtil.readInfoTemplate(templatePath)
            templateId = templateInfo['id']
            severity = templateInfo['severity']
        else:
            templateId = 'None'
            severity = 'None'

        templateIdTag = colored(str(templateId), "red")


        if str(info).__contains__("infected"):
            if severity.lower() == "critical" or severity.lower() == "high":
                severityTag = colored(str(severity), "red")
            elif severity.lower() == "medium":
                severityTag = colored(str(severity), "yellow")
            elif severity.lower() == "low":
                severityTag = colored(str(severity), "blue")
            else:
                severityTag = colored(str(severity), "green")
        else:
            severity = "None"
            severityTag = colored(str(severity), "green")

        print("[" + nowTag + "] " + "[" + targetUrlTag + "] " + "[" + templateIdTag + "] " + "[" + severityTag + "] " + infoTag)


    @staticmethod
    def printStartWarning():
        warningTag = colored("[WARNING]", "yellow", attrs=["underline"])
        print(warningTag + " Use with caution. You are responsible with your actions")
        print(warningTag + " Our developer team do not responsible for any misuse or damage")
        print(warningTag + " Please update our template repository regularly for latest CVEs")

    @staticmethod
    def getRaccoonMode():
        print("Gathering Mode")
        # print(" 1. Gathering target")
        # print(" 2. Scan with template")
        # mode = input("Select Raccoon mode: ")
        # if mode == "1":
        target = input("Enter domain/IP target: ")
        if target.strip().replace('.', '').isnumeric():
            return {"ip": target}
        elif validators.domain(target):
            return {"domain": target}
        else:
            errorTag = colored("[ERROR]", "red", attrs=["bold"])
            print(errorTag + "Invalid Domain/IP")
            return None
