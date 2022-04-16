import os, yaml

class TemplateUtil:
    @classmethod
    def readTemplate(self,config_content):
        try:
            isTemplateFileExist = os.path.isfile(config_content['templates'])
            if isTemplateFileExist:
                yaml_file = open(config_content['templates'],'r')
                yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
                return yaml_content
            else:
                print("Template file not found !!!!")
        except FileNotFoundError:
            print("Template file not found - File exception") 
    
    @classmethod
    def readRequestTemplate(self,config_content):
        yaml_content = self.readTemplate(config_content)
        requests_content = yaml_content['requests'][0]
        return requests_content

    @classmethod
    def readInfoTemplate(self,config_content):
        yaml_content = self.readTemplate()
        info_content = yaml_content['info']
        return info_content
