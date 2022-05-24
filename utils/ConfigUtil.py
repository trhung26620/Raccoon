import yaml
from pathlib import Path
from utils.TemplateUtil import TemplateUtil


class ConfigUtil:
    @staticmethod
    def readConfig():
        try:
            f_config = open(Path(__file__).parent /'..\config\config.yaml', 'r')
            config = yaml.load(f_config, Loader=yaml.FullLoader)
            return config
        except:
            try:
                f_config = open(Path(__file__).parent / '../config/config.yaml', 'r')
                config = yaml.load(f_config, Loader=yaml.FullLoader)
                return config
            except FileNotFoundError:
                print("Config file not found")
                exit()

    @staticmethod
    def filterTemplateWithId(ids, templatePathList):
        try:
            idList = ids.split(",")
            selectedTemplatePathList = list()
            for templatePath in templatePathList:
                info = TemplateUtil.readInfoTemplate(templatePath)
                if "id" not in info:
                    print("Detected the template with missing id information")
                    exit()
                for id in idList:
                    if info["id"] == id:
                        selectedTemplatePathList.append(templatePath)
                        break
            return selectedTemplatePathList
        except Exception as e:
            print("Error at function: filterTemplateWithId")
            print(e)

    @staticmethod
    def filterTemplateWithTag(tags, templatePathList):
        try:
            tagList = tags.split(",")
            selectedTemplatePathList = list()
            for templatePath in templatePathList:
                info = TemplateUtil.readInfoTemplate(templatePath)
                if "tags" in info:
                    for tag in tagList:
                        if tag in info["tags"].split(","):
                            selectedTemplatePathList.append(templatePath)
                            break
            return selectedTemplatePathList
        except Exception as e:
            print("Error at function: filterTemplateWithTag")
            print(e)

    @staticmethod
    def filterTemplateWithSeverity(severities, templatePathList):
        try:
            severityList = severities.split(",")
            selectedTemplatePathList = list()
            for templatePath in templatePathList:
                info = TemplateUtil.readInfoTemplate(templatePath)
                if "severity" not in info:
                    print("Detected the template with missing severity information")
                    exit()
                for severity in severityList:
                    if info["severity"] == severity:
                        selectedTemplatePathList.append(templatePath)
                        break
            return selectedTemplatePathList
        except Exception as e:
            print("Error at function: filterTemplateWithSeverity")
            print(e)

    @staticmethod
    def filterTemplateWithAuthor(authors, templatePathList):
        try:
            authorList = authors.split(",")
            selectedTemplatePathList = list()
            for templatePath in templatePathList:
                info = TemplateUtil.readInfoTemplate(templatePath)
                if "tags" in info:
                    for author in authorList:
                        if author in info["author"].split(","):
                            selectedTemplatePathList.append(templatePath)
                            break
            return selectedTemplatePathList
        except Exception as e:
            print("Error at function: filterTemplateWithAuthor")
            print(e)