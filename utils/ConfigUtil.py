import os, yaml
from pathlib import Path
from utils.TemplateUtil import TemplateUtil

class ConfigUtil:
    @staticmethod
    def readConfig():
        try:
            f_config = open(Path(__file__).parent /'..\config\config.yaml', 'r')
            config = yaml.load(f_config, Loader=yaml.FullLoader)
            return config
        except FileNotFoundError:
            print("Config file not found")

    @staticmethod
    def filterTemplateWithId(ids, templatePathList):
        idList = ids.split(",")
        selectedTemplatePathList = list()
        for templatePath in templatePathList:
            info = TemplateUtil.readInfoTemplate(templatePath)
            for id in idList:
                if info["id"] == id:
                    selectedTemplatePathList.append(templatePath)
                    break
        return selectedTemplatePathList

    @staticmethod
    def filterTemplateWithTag(tags, templatePathList):
        tagList = tags.split(",")
        selectedTemplatePathList = list()
        for templatePath in templatePathList:
            info = TemplateUtil.readInfoTemplate(templatePath)
            for tag in tagList:
                if tag in info["tags"].split(","):
                    selectedTemplatePathList.append(templatePath)
                    break
        return selectedTemplatePathList

    @staticmethod
    def filterTemplateWithSeverity(severities, templatePathList):
        severityList = severities.split(",")
        selectedTemplatePathList = list()
        for templatePath in templatePathList:
            info = TemplateUtil.readInfoTemplate(templatePath)
            for severity in severityList:
                if info["severity"] == severity:
                    selectedTemplatePathList.append(templatePath)
                    break
        return selectedTemplatePathList

    @staticmethod
    def filterTemplateWithAuthor(authors, templatePathList):
        authorList = authors.split(",")
        selectedTemplatePathList = list()
        for templatePath in templatePathList:
            info = TemplateUtil.readInfoTemplate(templatePath)
            for author in authorList:
                if author in info["author"].split(","):
                    selectedTemplatePathList.append(templatePath)
                    break
        return selectedTemplatePathList