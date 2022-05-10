import os
import string
import traceback
from bs4 import BeautifulSoup
import random
from utils import TemplateUtil
from models.HTMLReport import HTMLReport


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
                        payloadValues.append(payloadValue)
                return payloadValues
            else:
                print("File not found !!!")
                return None
        except FileNotFoundError:
            print("Can not read this file !!! ")
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
                print("Can not write to file - Invalid content - Written content must be string")
        except:
            print(traceback.format_exc())

    @staticmethod
    def printHTMLReport(listHTMLReportObject):
        if len(listHTMLReportObject) <= 0:
            print("[Debug - FileUtil] - Can not print report if there isn't any HTML Report object")
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

                        # append exposer
                        exposerContent[0].string = HTMLReportObj.exposer
                        # append injected payloads
                        injectedPayloads = HTMLReportObj.injectedPayload
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
                    print("Export HTML report to: " + os.path.abspath(htmlExportTemplateFile))
            else:
                print("Invalid path !!! Can not find template path: " + htmlTemplatePath)

        except:
            print(traceback.format_exc())
            return None




