# from msilib.schema import Component
from operator import mod
import os, yaml
from urllib.parse import urlparse
from re import template

class my_utils:
    @classmethod
    def readFile(self, mode_read):                  #mode: 1 to read only config, 2 to read template
        try:
            f_config = open('../config.yaml', 'r')
            config = yaml.load(f_config, Loader=yaml.FullLoader)

            if mode_read == 1:
                return config
            elif mode_read == 2:
                list_template = config['templates'] #when user use many teamplate at the same time
                list_result_template = list()

                for template in list_template:
                    try:                            #try catch for each template
                        f_template = open(template, 'r')
                        template_content = yaml.load(f_template, Loader=yaml.FullLoader)
                        list_result_template.append(template_content)               
                    except:
                        print("Template not found!!")
                    return list_result_template     #return a list of template (each template was read and returned to dict)
            else:
                print("only two mode: 1 or 2. Please try again!!")
        except:
            print("File not found - please try again!")

    @classmethod
    def replace_parameter(self):
        list_url = my_utils.readFile(1)['url']
        list_of_request = dict()
        list_of_components_url = my_utils.detached_of_url()

        for i in my_utils.readFile(2): #i['requests'][0]['request']: list of request
            for j in i['requests'][0]['request']:
                method = j.split()[0]
                for x in list_url:
                    # url = urlparse(x)
                    for z in list_of_components_url:
                        if (x == z['baseUrl']):
                            urlPattern = {
                                '{{BaseURL}}': z['baseUrl'],
                                '{{RootURL}}': z['rootUrl'],
                                '{{Hostname}}': z['host'],
                                '{{Host}}': z['hostname'],
                                '{{Port}}': str(z['port']),
                                '{{FullPath}}': z['fullPath'],
                                '{{Path}}': z['path'],
                                '{{File}}': z['file'],
                                '{{Scheme}}': z['scheme']
                            }
                            for k,v in urlPattern.items():
                                j = j.replace(k,v)
                            list_of_request[j] = method
        return list_of_request                              #return list + method

    @classmethod
    def detached_of_url(self):
        list_of_components_url = list()
        for i in my_utils.readFile(1)['url']:
            url = urlparse(i)
            components_url = {
                    'baseUrl': i,
                    'rootUrl': url.scheme + "://" + url.netloc,
                    'host' : url.netloc,
                    'port': url.port,
                    'hostname': url.hostname,
                    'fullPath': url.path + "?" + url.query,
                    'path': os.path.split(url.path)[0],
                    'file': os.path.split(url.path)[1],
                    'scheme': url.scheme,
                    'password': url.password,
                    'username': url.username,
                    'params': url.params
            }
            list_of_components_url.append(components_url)
        return list_of_components_url
                



        