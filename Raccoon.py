from services.CommandHandle import CommandUtil
from generator.TemplateConfigGenerator import TemplateConfigService
from services.RaccoonKernel import RaccoonKernel
from generator.RequestGenerator import RequestGenerator
import urllib3
from config.StaticData import Template
from utils.ConfigUtil import ConfigUtil
from config.StaticData import HTMLReportGlobal
from utils.FileUtil import FileUtil
from services.Debugger import Debugger
from config.StaticData import Debug
from utils.PrinterUtil import Printer
from services.EnumerateSubdomain import EnumSubdomain
from services.PortScanner import Scanner


urllib3.disable_warnings()

if __name__ == "__main__":
    args = CommandUtil()
    args.argument()
    args.argumentHandling()
    Printer.printStartWarning()
    Printer.printConfig()
    configValue = ConfigUtil.readConfig()
    isGatheringMode = configValue["Gathering-Mode"]
    # if isinstance(raccoonMode, dict):


    if isGatheringMode:
        raccoonMode = Printer.getRaccoonMode()
        if isinstance(raccoonMode, dict):
            if "domain" in raccoonMode:
                targetDomain = raccoonMode["domain"]
                Printer.printInfo("Scanning information at target: " + targetDomain + " ....")
                subList = EnumSubdomain.getFinalSubdomainList(raccoonMode["domain"])
                # print(subList)

                resolveIps = Scanner.resolveToIP(targetDomain)
                if len(resolveIps) != 0:
                    for ip in resolveIps:
                        Printer.printInfo(targetDomain + " resolve to: " + ip)
                    mainIp = resolveIps[0]
                else:
                    Printer.printInfo(targetDomain + " is not point to any ip address")

                runningServices = Scanner.getRunningService(mainIp)
                if len(runningServices) != 0:
                    Printer.printInfo("Running service on: " + mainIp + ":")
                    FileUtil.printHTMLInfoReport(runningServices, targetDomain, subList)
                else:
                    Printer.printInfo("No service running on: " + mainIp)

            elif "ip" in raccoonMode:
                targetIP = raccoonMode["ip"]
                subList = []
                runningServices = Scanner.getRunningService(targetIP)
                if len(runningServices) != 0:
                    Printer.printInfo("Running services on: " + targetIP + ":")
                    FileUtil.printHTMLInfoReport(runningServices, targetIP, subList)
                else:
                    Printer.printInfo("No service running on: " + targetIP)
        else:
            exit()
    # elif raccoonMode == 2:
    else:
        filePathList = configValue["templates"]
        for filePath in filePathList:
            Template.templatePath = filePath
            config = TemplateConfigService.getObjTemplateConfigByTemplate(Template.templatePath)
            requests = RequestGenerator.generateRequestObject(Template.templatePath)
            raccoon = RaccoonKernel()
            raccoon.raccoonFlowControl(config, requests)

        exportPath = configValue["output_file"]
        if len(HTMLReportGlobal.HTMLReportList) > 0 and exportPath:
            HTMLReportList = HTMLReportGlobal.HTMLReportList
            FileUtil.printHTMLReport(HTMLReportList, exportPath)

        if len(HTMLReportGlobal.HTMLReportList) == 0:
            Printer.printInfo("Scan complete - No vulnerability match your request")

        DebugInfo = Debug.DebugInfo
        if "debug" in configValue:
            Debugger.debugCall(DebugInfo)





