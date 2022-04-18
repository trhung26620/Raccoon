import os, yaml
from os import walk
from utils.ConfigUtil import ConfigUtil


class TemplateUtil:
    @classmethod
    def readTemplate(self):
        config_content = ConfigUtil().readConfig()
        try:
            isTemplateFileExist = os.path.isfile(config_content['templates'])
            if isTemplateFileExist:
                yaml_file = open(config_content['templates'], 'r')
                yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
                return yaml_content
            else:
                isFolderExist = os.path.isdir(config_content['templates'])
                template_dict = {}
                if isFolderExist:
                    template_files = []
                    for (dirpath, dirnames, filenames) in walk(config_content['templates']):
                        template_files.extend(filenames)
                        break
                    for template_file in template_files:
                        template_path = config_content['templates'] + template_file
                        yaml_file = open(template_path, 'r')
                        yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        template_dict[template_file] = yaml_content
                    return template_dict
                else:
                    print("Template file or Folder not found !!!!")
        except FileNotFoundError:
            print("Template file or Folder not found - File/Folder exception")

    @classmethod
    def readRequestTemplate(self, config_content):
        yaml_content = self.readTemplate(config_content)
        requests_content = yaml_content['requests'][0]
        return requests_content

    @classmethod
    def readInfoTemplate(self, config_content):
        yaml_content = self.readTemplate()
        info_content = yaml_content['info']
        return info_content
