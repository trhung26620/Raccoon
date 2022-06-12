import os
import string
import traceback
from bs4 import BeautifulSoup
import random
from utils import TemplateUtil
from termcolor import colored, cprint
from utils.PrinterUtil import Printer
from config.StaticData import Subdomain


class FileUtil:
    @staticmethod
    def getWordlistPath():
        dirname = os.path.dirname(__file__)
        try:
            wordlistPath = os.path.join(dirname, f"../config/{Subdomain.wordListFileName}")
            return wordlistPath
        except:
            try:
                wordlistPath = os.path.join(dirname, f"..\config\{Subdomain.wordListFileName}")
                return wordlistPath
            except FileNotFoundError:
                Printer.printError("Wordlist file not found")
                exit()

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
                        payloadValues.append(payloadValue)
                return payloadValues
            else:
                Printer.printError("Payload file not found")
                return None
        except FileNotFoundError:
            Printer.printError("Can not read this file: " + filePath)
            fileObject.close()
            return None

    @staticmethod
    def getRandomString(length):
        letters = string.ascii_lowercase
        resultStr = ''.join(random.choice(letters) for i in range(length))
        return resultStr

    @staticmethod
    def writeToFile(filePath, content):
        try:
            fileObject = open(filePath, "w+")
            if type(content) is str:
                fileObject.write(content)
                fileObject.close()
            else:
                Printer.printError("Can not write to file - Invalid content - Written content must be string")
        except:
            # print(traceback.format_exc())
            Printer.printError("Can not write to file - Something wrong happen!")

    @staticmethod
    def printHTMLReport(listHTMLReportObject):
        if len(listHTMLReportObject) <= 0:
            return None
        try:
            htmlTemplatePath = "reportTemplate" + os.sep + "html" + os.sep + "report.html"
            exportDirectory = os.path.exists(htmlTemplatePath)
            if exportDirectory:
                with open(htmlTemplatePath) as fp:
                    soup = BeautifulSoup(fp, "html.parser")
                    reportContainer = soup.select_one("#container")     # container class contain all report frame
                    for HTMLReportIndex, HTMLReportObj in enumerate(listHTMLReportObject):
                        reportFrames = soup.find_all("ol", {"class": "reportList"})  # find all report frame and put to a list every time
                        if HTMLReportIndex > (len(reportFrames) - 1):
                            break

                        currentHTMLFrame = reportFrames[HTMLReportIndex]
                        targetTags = currentHTMLFrame.find_all("span", {"class": "target"})
                        idTags = currentHTMLFrame.find_all("span", {"class": "id"})
                        nameTags = currentHTMLFrame.find_all("span", {"class": "name"})
                        authorTags = currentHTMLFrame.find_all("span", {"class": "author"})
                        severityTags = currentHTMLFrame.find_all("span", {"class": "severity"})
                        descriptionTags = currentHTMLFrame.find_all("span", {"class": "description"})
                        remediationTags = currentHTMLFrame.find_all("span", {"class": "remediation"})
                        referenceList = currentHTMLFrame.find_all("div", {"class": "reference"})
                        tagTags = currentHTMLFrame.find_all("span", {"class": "tags"})
                        exposerContent = currentHTMLFrame.find_all("div", {"class": "exposerContent"})
                        payloadsContent = currentHTMLFrame.find_all("div", {"class": "listPayloads"})

                        templatePath = HTMLReportObj.templateFilePath
                        templateInfo = TemplateUtil.TemplateUtil.readInfoTemplate(templatePath)

                        # append content in HTML
                        # append info
                        if "id" in templateInfo:
                            idTags[0].string = templateInfo["id"]
                        else:
                            idTags[0].string = ""
                        if "name" in templateInfo:
                            nameTags[0].string = templateInfo["name"]
                        else:
                            nameTags[0].string = ""
                        if "author" in templateInfo:
                            authorTags[0].string = templateInfo["author"]
                        else:
                            authorTags[0].string = ""
                        if "severity" in templateInfo:
                            severityTags[0].string = templateInfo["severity"]
                        else:
                            severityTags[0].string = ""
                        if "description" in templateInfo:
                            descriptionTags[0].string = templateInfo["description"]
                        else:
                            descriptionTags[0].string = ""
                        if "remediation" in templateInfo:
                            remediationTags[0].string = templateInfo["remediation"]
                        else:
                            remediationTags[0].string = ""
                        if "reference" in templateInfo:
                            for reference in templateInfo["reference"]:
                                appendStr = "- " + reference + "<br>"
                                referenceList[0].append(BeautifulSoup(appendStr, "html.parser"))
                        else:
                            referenceList[0].string = ""
                        if "tags" in templateInfo:
                            tagTags[0].string = templateInfo["tags"]
                        else:
                            tagTags[0].string = ""

                        # reset content of each tag before append new content
                        exposerContent[0].string = ""
                        payloadsContent[0].string = ""
                        targetTags[0].string = ""

                        # append target url
                        targetTags[0].string = HTMLReportObj.target
                        # append exposer
                        listExposer = HTMLReportObj.exposer
                        if len(listExposer) == 0:
                            exposerContent[0].string = "- No exposer was specify"
                        else:
                            for exposer in listExposer:
                                appendedExposer = "- " + str(exposer) + "<br>"
                                exposerContent[0].append(BeautifulSoup(appendedExposer, "html.parser"))
                        # append injected payloads
                        injectedPayloads = HTMLReportObj.injectedPayload
                        if len(injectedPayloads) == 0:
                            payloadsContent[0].string = "- No payload was specify"
                        else:
                            for payloadKey in injectedPayloads:
                                appendedPayload = "- " + payloadKey + ": " + injectedPayloads[payloadKey] + "<br>"
                                payloadsContent[0].append(BeautifulSoup(appendedPayload, "html.parser"))

                        appendedContent = str(currentHTMLFrame).replace("&nbsp", "")   # delete new line character to append HTML content
                        reportContainer.append(BeautifulSoup(appendedContent, "html.parser"))

                    # delete final frame
                    reportFrames = soup.find_all("ol", {"class": "reportList"})
                    finalFrame = reportFrames[len(reportFrames) - 1]
                    for childTag in finalFrame:
                        try:
                            childTag.decompose()
                        except:
                            pass
                    finalFrame.decompose()

                    # export to file
                    randomFileName = "RaccoonReport_" + FileUtil.getRandomString(10) + ".html"
                    htmlExportTemplateFile = "reportTemplate" + os.sep + "html" + os.sep + randomFileName
                    FileUtil.writeToFile(htmlExportTemplateFile, str(soup))
                    cprint("[Info] - Export HTML report to: " + os.path.abspath(htmlExportTemplateFile), "yellow")
            else:
                Printer.printError("Invalid path !!! Can not find template path: " + htmlTemplatePath)

        except:
            print(traceback.format_exc())
            return None




