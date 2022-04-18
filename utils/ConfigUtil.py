import os, yaml

class ConfigUtil:
    def readConfig(self):
        try:
            isConfigFileExist = os.path.isfile("config.yaml")
            if isConfigFileExist:
                config_file = open("config.yaml",'r')
                config_content = yaml.load(config_file, Loader=yaml.FullLoader)
                return config_content
            else:
                print("Config file not found !!!!")

        except FileNotFoundError:
            print("Config file not found - File exception")