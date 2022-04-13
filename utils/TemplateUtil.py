import os, yaml

class TemplateUtil:
    def __init__(self):
        self.args = None
    
    def readTemplate(self):
        try:
            isConfigFileExist = os.path.isfile("../config.yaml")
            if isConfigFileExist:
                config_file = open("../config.yaml",'r')
                config_content = yaml.load(config_file, Loader=yaml.FullLoader)
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
            else:
                print("Config file not found !!!!")

        except FileNotFoundError:
            print("Config file not found - File exception")
    
    def readRequestTemplate(self):
        yaml_content = self.readTemplate()
        requests_content = yaml_content['requests'][0]
        return requests_content['request']     

    def readInfoTemplate(self):
        yaml_content = self.readTemplate()
        info_content = yaml_content['info']
        return info_content
                    