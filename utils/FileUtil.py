import os
import string
import traceback
from bs4 import BeautifulSoup
import random
from utils import TemplateUtil
from termcolor import colored, cprint
from utils.PrinterUtil import Printer
from config.StaticData import Subdomain
from config.StaticData import SeverityCounter


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
                Printer.printError("Wordlist file not found: " + str(wordlistPath))
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
                Printer.printError("Payload file not found: " + str(filePath))
                exit()
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
    def appendDrawChartFunctionNameJS(infoStat, lowStat, mediumStat, highStat, criticalStat):
        functionName = "drawSeverityChart(" + str(infoStat) + ", " + str(lowStat) + ", " + str(mediumStat) + ", " + str(highStat) + ", " + str(criticalStat) + ")"
        return functionName


    @staticmethod
    def printHTMLReport(listHTMLReportObject, exportPath):
        if len(listHTMLReportObject) <= 0:
            return None
        try:
            htmlTemplatePath = "reportTemplate" + os.sep + "html" + os.sep + "report.html"
            isExportPath = os.path.exists(exportPath)
            if isExportPath:
                with open(htmlTemplatePath) as fp:
                    soup = BeautifulSoup(fp, "html.parser")

                    # draw severity chart
                    functionName = FileUtil.appendDrawChartFunctionNameJS(SeverityCounter.infoSeverityCounter, SeverityCounter.lowSeverityCounter, SeverityCounter.mediumSeverityCounter, SeverityCounter.highSeverityCounter, SeverityCounter.criticalSeverity)
                    bodyTag = soup.find_all('body')
                    bodyTag[0].attrs['onload'] = functionName

                    # append information
                    reportContainer = soup.select_one("#container")     # container class contain all report frame
                    for HTMLReportIndex, HTMLReportObj in enumerate(listHTMLReportObject):
                        reportFrames = soup.find_all("ol", {"class": "reportList"})  # find all report frame and put to a list every time
                        if HTMLReportIndex > (len(reportFrames) - 1):
                            break

                        currentHTMLFrame = reportFrames[HTMLReportIndex]
                        targetTags = currentHTMLFrame.find_all("a", {"class": "target"})
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
                            # add color to severity tag
                            severityContent = templateInfo["severity"]
                            if str(severityContent).lower() == "critical":
                                severityTags[0].attrs['style'] = 'color: red; font-weight: bold'
                            elif str(severityContent).lower() == "high":
                                severityTags[0].attrs['style'] = 'color: orange; font-weight: bold'
                            elif str(severityContent).lower() == "medium":
                                severityTags[0].attrs['style'] = 'color: yellow; font-weight: bold'
                            elif str(severityContent).lower() == "low":
                                severityTags[0].attrs['style'] = 'color: green; font-weight: bold'
                            elif str(severityContent).lower() == "info":
                                severityTags[0].attrs['style'] = 'color: grey; font-weight: bold'
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

                        referenceList[0].string = ""
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
                        targetTags[0].attrs['href'] = HTMLReportObj.target

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
                    htmlExportTemplateFile = exportPath + os.sep + randomFileName
                    FileUtil.writeToFile(htmlExportTemplateFile, str(soup))
                    cprint("[Info] - Export HTML report to: " + os.path.abspath(htmlExportTemplateFile), "yellow")
            else:
                Printer.printError("Invalid path !!! Can not export to path: " + exportPath)

        except:
            print(traceback.format_exc())
            return None


    @staticmethod
    def printHTMLInfoReport(listInfoDict, target, subDomains, wpVersion):

        if len(listInfoDict) <= 0:
            Printer.printError("Can not print report")
            return

        htmlTemplatePath = "reportTemplate" + os.sep + "html" + os.sep + "information.html"
        exportDirectory = os.path.exists(htmlTemplatePath)
        if not exportDirectory:
            Printer.printInfo("Path " + str(htmlTemplatePath) + " does not exist")
            return
        with open(htmlTemplatePath) as fp:
            soup = BeautifulSoup(fp, "html.parser")
            reportContainer = soup.select_one("#container")  # container class contain all report frame

            # append sub-domains
            subDomainContent = soup.find_all("div", {"class": "subDomains"})
            if len(subDomains) <= 0:
                subDomainContent[0].string = "No sub domain was found"
            else:
                for subDomain in subDomains:
                    appendedSubDomain = "- " + str(subDomain) + "<br>"
                    subDomainContent[0].append(BeautifulSoup(appendedSubDomain, "html.parser"))

            # append wordpress version
            moreInfoTags = soup.find_all("span", {"class": "moreInfo"})
            if wpVersion is not None:
                moreInfoTags[0].string = str(wpVersion)
            else:
                moreInfoTags[0].string = "No additional information was detected"

            # append service detail
            for HTMLReportIndex, serviceDict in enumerate(listInfoDict):
                reportFrames = soup.find_all("ol", {"class": "reportList"})   # find all report frame and put to a list every time
                if HTMLReportIndex > (len(reportFrames) - 1):
                    break

                currentHTMLFrame = reportFrames[HTMLReportIndex]
                targetTags = currentHTMLFrame.find_all("span", {"class": "target"})
                portTags = currentHTMLFrame.find_all("span", {"class": "port"})
                conTypeTags = currentHTMLFrame.find_all("span", {"class": "conType"})
                stateTags = currentHTMLFrame.find_all("span", {"class": "state"})
                serviceTags = currentHTMLFrame.find_all("span", {"class": "service"})
                serviceNameTags = currentHTMLFrame.find_all("span", {"class": "serviceName"})
                versionTags = currentHTMLFrame.find_all("span", {"class": "version"})
                targetTags[0].string = target



                for port, services in listInfoDict[HTMLReportIndex].items():
                    portTags[0].string = str(port)
                    conTypeTags[0].string = services["reason"]
                    stateTags[0].string = services["state"]
                    serviceTags[0].string = services["name"]
                    serviceNameTags[0].string = services["product"]
                    versionTags[0].string = services["version"]


                # delete new line character to append HTML content
                appendedContent = str(currentHTMLFrame).replace("&nbsp", "")
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
            randomFileName = "RaccoonReportInformation_" + FileUtil.getRandomString(10) + ".html"
            htmlExportTemplateFile = "reportTemplate" + os.sep + "html" + os.sep + randomFileName
            FileUtil.writeToFile(htmlExportTemplateFile, str(soup))
            cprint("[Info] - Export HTML report to: " + os.path.abspath(htmlExportTemplateFile), "yellow")










