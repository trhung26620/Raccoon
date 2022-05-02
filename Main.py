from scanner.CommandHandle import CommandUtil
from generator.TemplateConfigGenerator import TemplateConfigService
from scanner.RaccoonKernel import RaccoonKernel
from generator.RequestGenerator import RequestGenerator
import urllib3
from config.StaticData import Template
from utils.ConfigUtil import ConfigUtil

urllib3.disable_warnings()

if __name__ == "__main__":
    args = CommandUtil()
    args.argument()
    args.argumentHandling()
    filePathList = ConfigUtil.readConfig()["templates"]
    for filePath in filePathList:
        Template.templatePath = filePath
        config = TemplateConfigService.getObjTemplateConfigByTemplate(Template.templatePath)
        requests = RequestGenerator.generateRequestObject(Template.templatePath)
        raccoon = RaccoonKernel()
        raccoon.raccoonFlowControl(config, requests)
