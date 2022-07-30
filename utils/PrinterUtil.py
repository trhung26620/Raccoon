from termcolor import colored
from datetime import datetime
import validators
import os


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
    def printScanResult(targetUrl, payload, exposer, result, templatePath):
        now = datetime.now()
        nowTag = colored(str(now), "cyan", attrs=["bold"])
        targetUrlTag = colored(str(targetUrl), "blue", attrs=["bold"])
        exposerTag = colored("Exposer:" + str(exposer), "cyan", attrs=["bold"])
        finalStr = "[" + nowTag + "]" + "[" + targetUrlTag + "]"

        if str(templatePath).strip() != '':
            from utils.TemplateUtil import TemplateUtil
            templateInfo = TemplateUtil.readInfoTemplate(templatePath)
            templateId = templateInfo['id']
            severity = templateInfo['severity']
        else:
            templateId = 'None'
            severity = 'None'
        templateIdTag = colored(str(templateId), "red", attrs=["bold"])
        finalStr += "[" + templateIdTag + "]"

        if result:
            if severity.lower() == "critical" or severity.lower() == "high":
                severityTag = colored(str(severity), "red", attrs=["bold"])
            elif severity.lower() == "medium":
                severityTag = colored(str(severity), "yellow", attrs=["bold"])
            elif severity.lower() == "low":
                severityTag = colored(str(severity), "blue", attrs=["bold"])
            else:
                severityTag = colored(str(severity), "green", attrs=["bold"])
            finalStr += "[" + severityTag + "]"

            if payload is not None:
                infoTag = colored("Payload: " + str(payload), "red", attrs=["bold"])
                finalStr += "[" + infoTag + "]"
            else:
                infoTag = ""
            if len(exposer) > 1 and None not in exposer and exposer is not None:
                finalStr += "[" + exposerTag + "]"
        else:
            # severity = "None"
            # severityTag = colored(str(severity), "green", attrs=["bold"])
            # finalStr += "[" + severityTag + "]"
            infoTag = colored("Target is negative", "green", attrs=["bold"])
            finalStr += "[" + infoTag + "]"

        print("\n" + finalStr)


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
                print("- Template path: " + os.path.abspath(template))

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

        #print export path
        if "output_file" in config and config["output_file"] is not None:
            exportPath = config["output_file"]
            print(configTag + " Export path: " + os.path.abspath(str(exportPath)))
        else:
            print(configTag + " Export path: No path was specify")


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


