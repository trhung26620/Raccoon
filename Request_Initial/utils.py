import yaml
class utils:

    @staticmethod
    def readConfigFile():
        config_file = open("../config.yaml",'r')
        config_content = yaml.load(config_file, Loader=yaml.FullLoader)
        return config_content
    def readTemplate():
        template_content = yaml.load("../", Loader=yaml.FullLoader)
        return template_content


print(utils.readConfigFile())