import os, yaml

class TemplateUtil:
    @staticmethod
    def readTemplate(templateFilePath):
        try:
            f_template = open(templateFilePath, 'r')
            template_content = yaml.load(f_template, Loader=yaml.FullLoader)
            return template_content
        except FileNotFoundError:
            print("Template not found!!")

    @staticmethod
    def readRequestTemplate(templateFilePath):
        yaml_content = TemplateUtil.readTemplate(templateFilePath)
        requests_content = yaml_content['requests'][0]
        return requests_content

    @staticmethod
    def readInfoTemplate(templateFilePath):
        yaml_content = TemplateUtil.readTemplate(templateFilePath)
        info_content = yaml_content['info']
        return info_content
