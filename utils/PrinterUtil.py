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


        if str(info).lower().__contains__("payload"):
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
    def printConfig():
        from utils.ConfigUtil import ConfigUtil

        configTag = colored("[CONFIG]", "yellow", attrs=["underline"])
        config = ConfigUtil.readConfig()

        # print used template
        if "templates" in config and len(config["templates"]) != 0:
            usedTemplates = config["templates"]
            print(configTag + " Template used: ")
            for template in usedTemplates:
                print("- Template path: " + template)

        else:
            print(configTag + " No template was specify")

        # print proxy
        if "proxy" in config:
            proxyValue = config["proxy"]
            print(configTag + " Proxy:  " + str(proxyValue))
        else:
            print(configTag + " No proxy was specify")

        # print debug
        if "debug" in config and config["debug"] is not None:
            debugMode = config["debug"]
            print(configTag + " Debug mode: " + str(debugMode))
        else:
            print(configTag + " Debug mode: No")

        # print verbose
        if "verbose" in config and config["verbose"] is True:
            print(configTag + " Verbose: yes")
        else:
            print(configTag + " Verbose: no")

        # print mode
        if "Gathering-Mode" in config and config["Gathering-Mode"] is True:
            print(configTag + " Raccoon Mode: gathering")
        else:
            print(configTag + " Raccoon Mode: custom")


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


