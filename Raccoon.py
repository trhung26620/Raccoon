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
    raccoonMode = Printer.getRaccoonMode()
    if isinstance(raccoonMode, dict):
        if "domain" in raccoonMode:
            targetDomain = raccoonMode["domain"]
            Printer.printInfo("Scanning information at target: " + targetDomain)
            subList = EnumSubdomain.getFinalSubdomainList(raccoonMode["domain"])
            print(subList)
    elif raccoonMode == 2:
        args = CommandUtil()
        args.argument()
        args.argumentHandling()
        Printer.printStartWarning()

        configValue = ConfigUtil.readConfig()
        filePathList = configValue["templates"]

        for filePath in filePathList:
            Template.templatePath = filePath
            config = TemplateConfigService.getObjTemplateConfigByTemplate(Template.templatePath)
            requests = RequestGenerator.generateRequestObject(Template.templatePath)
            raccoon = RaccoonKernel()
            raccoon.raccoonFlowControl(config, requests)

        if len(HTMLReportGlobal.HTMLReportList) > 0:
            HTMLReportList = HTMLReportGlobal.HTMLReportList
            FileUtil.printHTMLReport(HTMLReportList)

        DebugInfo = Debug.DebugInfo
        if "debug" in configValue:
            Debugger.debugCall(DebugInfo)





