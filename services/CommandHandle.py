import argparse, yaml
import os
import glob
from utils.ConfigUtil import ConfigUtil
from utils.DisplayUtil import DisplayUtil
from config.StaticData import DefaultRequestFiringConfig
from config.StaticData import AboutUs
from colorama import Fore, Back, Style

class CommandUtil:
    def __init__(self):
        self.args = None

    def argument(self):
        parser = argparse.ArgumentParser(description=DisplayUtil.displayBanner())
        parser.add_argument("--gathering", "-g", help="Raccoon will gather information about the target like subdomain, port, services,...", required=False, action="store_true")
        parser.add_argument("--target", "-u", help="Specify a URL to scan.", required=False)
        parser.add_argument("--list", "-l", help="Specify path to file containing a list of target URLs to scan (one per line)", required=False)
        parser.add_argument("--templates", "-t", help="Template or template directory paths to include in the scan", required=False)
        parser.add_argument("--it", help="Specify templates based on IDs. (e.g. CVE-2021-44228,iis-shortname)", required=False)
        parser.add_argument("--tag", help="Specify templates based on tags. (e.g. cve,fuzz). ", required=False)
        parser.add_argument("--severity", "-s",help="Specify templates based on severities. Possible values: info, low, medium, high, critical.", required=False)
        parser.add_argument("--author", "-a",help="Execute templates that are (co-)created by the specified authors.", required=False)
        parser.add_argument("--output-file", "-o", help="Specify file path to write info and result during scanning to a file.", required=False)
        parser.add_argument("--thread", "-T", help="Max number of concurrent HTTP(s) requests (default 10)", required=False)
        parser.add_argument("--interactsh-server", "-is", help="Specify an interactsh server url for self-hosted instance. (Warning: We can not analyze or parse result with this option)", required=False)
        parser.add_argument("--timeout", help="Time to wait in seconds before timeout (default 10).", required=False)
        parser.add_argument("--retries", help="Number of times to retry a failed request (default 0).", required=False)
        parser.add_argument("--debug", help="Show all requests and responses.", required=False, action="store_true")
        parser.add_argument("--debug-req", help="Show all sent requests.", required=False, action="store_true")
        parser.add_argument("--debug-resp", help="Show all received responses.", required=False, action="store_true")
        parser.add_argument("--proxy", "-p", help="Use a proxy to connect to the target URL (e.g. \"http://127.0.0.1:8080\").", required=False)
        parser.add_argument("--version", help="Show the version of tool.", required=False, action="store_true")
        parser.add_argument("--verbose", "-v", help="Show verbose output.", required=False, action="store_true")
        # parser.add_argument("--update-templates", "-ut", help="Update Powerscanner-templates to latest released version.", required=False)
        self.args = parser.parse_args()

    def argumentHandling(self):
        config_yaml = {}
        # if self.args.update_templates:
        #     config_yaml['update_templates'] = self.args.update_templates

        if self.args.version:
            print(f"{Fore.CYAN}{AboutUs.version}"+"\n")
            exit()
        if self.args.gathering:
            config_yaml['Gathering-Mode'] = True
        else:
            config_yaml['Gathering-Mode'] = False
            if self.args.list:
                urlFile = open(self.args.list, "r")
                urlList = urlFile.read().split("\n")
                config_yaml['url'] = urlList
            elif self.args.target:
                config_yaml['url'] = [self.args.target]
            else:
                print("Please provide URL")
                exit()
            if self.args.templates:
                path = self.args.templates
                if os.path.isdir(path):
                    files = glob.glob(path + '/**/*.yaml', recursive=True)
                    config_yaml['templates'] = files
                elif os.path.isfile(path) and path.endswith(".yaml"):
                    config_yaml['templates'] = [path]
                else:
                    print("invalid file")
            else:
                print("Please provide template")
                exit()
            if self.args.it:
                config_yaml["templates"] = ConfigUtil.filterTemplateWithId(self.args.it, config_yaml["templates"])
            else:
                if self.args.tag:
                    config_yaml["templates"] = ConfigUtil.filterTemplateWithTag(self.args.tag, config_yaml["templates"])
                if self.args.severity:
                    config_yaml["templates"] = ConfigUtil.filterTemplateWithSeverity(self.args.severity, config_yaml["templates"])

                if self.args.author:
                    config_yaml["templates"] = ConfigUtil.filterTemplateWithAuthor(self.args.author, config_yaml["templates"])

            if self.args.output_file:
                config_yaml["output_file"] = self.args.output_file
            else:
                config_yaml["output_file"] = None

            if self.args.thread:
                config_yaml['thread'] = self.args.thread
            else:
                config_yaml['thread'] = None

            if self.args.interactsh_server:
                config_yaml['interactsh_server'] = self.args.interactsh_server
            else:
                config_yaml['interactsh_server'] = None

            if self.args.timeout:
                config_yaml['timeout'] = self.args.timeout
            else:
                config_yaml['timeout'] = DefaultRequestFiringConfig.defaultTimeout

            if self.args.retries:
                config_yaml['retries'] = self.args.retries
            else:
                config_yaml['retries'] = 0

            if self.args.debug:
                config_yaml['debug'] = "debug"
            elif self.args.debug_req:
                config_yaml['debug'] = "debug_req"
            elif self.args.debug_resp:
                config_yaml['debug'] = "debug_resp"
            else:
                config_yaml['debug'] = None
            if self.args.proxy:
                config_yaml['proxy'] = {
                    "http": self.args.proxy,
                    "https": self.args.proxy
                }
            else:
                config_yaml['proxy'] = {}

            if self.args.verbose:
                config_yaml['verbose'] = self.args.verbose
            else:
                config_yaml['verbose'] = False

        configFilePath = os.path.join('config', 'config.yaml')
        with open(configFilePath, 'w') as file:
            documents = yaml.dump(config_yaml, file)

