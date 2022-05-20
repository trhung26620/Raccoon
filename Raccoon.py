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


urllib3.disable_warnings()

if __name__ == "__main__":
    args = CommandUtil()
    args.argument()
    args.argumentHandling()

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





