import os
import string
import traceback
from bs4 import BeautifulSoup
import random
from models.HTMLReport import HTMLReport
from utils import TemplateUtil


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
                print("Export HTML report to: " + htmlTemplatePath)
                # htmlTemplatePath = r"reportTemplate/html/report.html"

                with open(htmlTemplatePath) as fp:
                    soup = BeautifulSoup(fp, "html.parser")
                    reportContainer = soup.select_one("#container")     # container class contain all report
                    reportFrames = soup.find_all("ol", {"class": "reportList"})   # first report frame
                    for HTMLReportIndex, HTMLReportObj in enumerate(listHTMLReportObject):
                        if HTMLReportIndex >= len(reportFrames):
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

                        templatePath = HTMLReportObj.templateFilePath
                        templateInfo = TemplateUtil.TemplateUtil.readInfoTemplate(templatePath)

                        if "id" in templateInfo:
                            idTags[HTMLReportIndex].string = templateInfo["id"]
                        if "name" in templateInfo:
                            nameTags[HTMLReportIndex].string = templateInfo["name"]
                        if "author" in templateInfo:
                            authorTags[HTMLReportIndex].string = templateInfo["author"]
                        if "severity" in templateInfo:
                            severityTags[HTMLReportIndex].string = templateInfo["severity"]
                        if "description" in templateInfo:
                            descriptionTags[HTMLReportIndex].string = templateInfo["description"]
                        if "remediation" in templateInfo:
                            remediationTags[HTMLReportIndex] = templateInfo["remediation"]
                        if "reference" in templateInfo:
                            for reference in templateInfo["reference"]:
                                appendStr = "- " + reference + "<br>"
                                referenceList[HTMLReportIndex].append(BeautifulSoup(appendStr, "html.parser"))
                        if "tags" in templateInfo:
                            tagTags[HTMLReportIndex].string = templateInfo["tags"]
                        exposerContent[HTMLReportIndex].string = HTMLReportObj.exposer

                        appendedContent = str(currentHTMLFrame).replace("&nbsp", "")   # delete new line character
                        reportContainer.append(BeautifulSoup(appendedContent, "html.parser"))
                    # print(soup)
                    isDir = os.path.isdir(htmlTemplatePath)
                    if isDir:
                        randomFileName = "RaccoonReport_" + FileUtil.getRandomString(10) + ".html"
                        htmlTemplatePath += os.sep + randomFileName
                        FileUtil.writeToFile(htmlTemplatePath, str(soup))
            else:
                print("Invalid path !!! Can not export to this path: " + htmlTemplatePath)

        except:
            print(traceback.format_exc())
            return None




