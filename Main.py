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

       # Test export to HTML file
    # listHTMLReportObject = []
    # HTMLReportObject1 = HTMLReport("template/demo template/addBodyJsonAndQueryToCVE44228.yaml", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas viverra ligula justo, ultrices maximus leo rutrum dapibus. Pellentesque in sem id lectus sodales aliquet at tempor metus. Maecenas scelerisque dolor ac orci semper porttitor. Sed sed eros ipsum. Etiam at nulla a nisl convallis fringilla et quis diam. Aliquam molestie augue elit, a gravida metus condimentum vitae. Pellentesque quis quam tortor. Proin sit amet pulvinar orci. Maecenas et suscipit neque. Nam dapibus eget felis id placerat. Pellentesque ultricies metus nibh, nec fringilla ex euismod feugiat. Ut et magna elit. Donec eget dui aliquet, venenatis felis nec, vestibulum ipsum. Integer at sem in turpis mollis suscipit. Vestibulum elementum neque ac mi gravida, id varius tellus molestie.")
    # HTMLReportObject2 = HTMLReport("template/demo template/test.yaml", "Donec dictum augue libero, et lobortis risus lacinia eget. Mauris lobortis sem vitae nunc dapibus vulputate vitae a sapien. Donec a libero porttitor, tempor odio in, venenatis nisl. Fusce gravida quam lectus, sed facilisis dui facilisis vel. Phasellus vel posuere nibh. Sed ullamcorper sem quis scelerisque consequat. Phasellus vitae rhoncus lectus, id accumsan justo. Phasellus et orci est. Ut finibus elit quis dignissim consectetur. Phasellus a accumsan nunc, id ornare elit. Nulla pellentesque, dui ut scelerisque tristique, dolor nunc malesuada neque, eu accumsan metus lorem quis dui. Nulla mollis imperdiet nisi sit amet pulvinar. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;")
    # listHTMLReportObject.append(HTMLReportObject1)
    # listHTMLReportObject.append(HTMLReportObject2)
    #
    # FileUtil.printHTMLReport(listHTMLReportObject)
