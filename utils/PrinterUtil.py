from termcolor import colored
from datetime import datetime


class Printer:

    @staticmethod
    def printError(err):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        errorTag = colored("[ERROR]", "red", attrs=["bold"])
        print("\n[" + nowTag + "] " + errorTag + " " + str(err))


    @staticmethod
    def printWarning(warning):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        warningTag = colored("[WARNING]", "yellow", attrs=["underline"])
        print("\n[" + nowTag + "] " + warningTag + " " + str(warning))


    @staticmethod
    def printInfo(info):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        infoTag = colored("[INFO]", "blue", attrs=["underline"])
        print("\n[" + nowTag + "] " + infoTag + " " + str(info))

    @staticmethod
    def printScanResult(targetUrl, info, result):
        now = datetime.now()
        nowTag = colored(str(now), "cyan")
        targetUrlTag = colored(str(targetUrl), "blue")
        if result:
            infoTag = colored(info, "red")
        else:
            infoTag = colored(info, "green")

        print("[" + nowTag + "] " + "[" + targetUrlTag + "] " + infoTag)


    @staticmethod
    def printStartWarning():
        warningTag = colored("[WARNING]", "yellow", attrs=["underline"])
        print(warningTag + " Use with caution. You are responsible with your actions")
        print(warningTag + " Our developer team do not responsible for any misuse or damage")
        print(warningTag + " Please update our template repository regularly for latest CVEs")



