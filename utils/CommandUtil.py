import yaml, argparse

class CommandUtil:
    def __init__(self):
        self.args = None

    def argument(self):
        description = "Xin chao, day la tool tiem lo hong."
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("-target", "-u", help="Specify a URL/Hosts to scan.", required=False)
        parser.add_argument("--list", "-l", help="Specify path to file containing a list of target URLs/hosts to scan (one per line)", required=False, action="store_true")
        parser.add_argument("--templates", "-t", help="Template or template directory paths to include in the scan", required=False)
        parser.add_argument("--it", help="ID template.", required=False)
        parser.add_argument("--tag", help="Tag template.", required=False)
        parser.add_argument("--severity", "-s",help="Templates to run based on severity. Possible values: info, low, medium, high, critical.", required=False)
        parser.add_argument("--author", "-a",help="Execute templates that are (co-)created by the specified authors.", required=False)
        parser.add_argument("--output-file", "-o", help="Write an output to a file.", required=False)
        parser.add_argument("--include-rr", "-irr", help="Include request/response pairs in the JSONL output (for findings only).", required=False)
        parser.add_argument("---thread", "-T", help="Max number of concurrent HTTP(s) requests (default 10)", required=False)
        parser.add_argument("--interactsh-server", "-is", help="Specify an interactsh server url for self-hosted instance (default: oast.pro,oast.live,oast.site,oast.online,oast.fun,oast.me).", required=False)
        parser.add_argument("--timeout", help="Time to wait in seconds before timeout (default 5).", required=False)
        parser.add_argument("--retries", help="Number of times to retry a failed request (default 1).", required=False)
        parser.add_argument("--debug", help="Show all requests and responses.", required=False)
        parser.add_argument("--debug-req", help="Show all sent requests.", required=False)
        parser.add_argument("--debug-resp", help="Show all received responses.", required=False)
        parser.add_argument("--proxy", "-p", help="Inject interact-sh server to payloads.", required=False, action="store_true")
        parser.add_argument("--version", help="Show the version of tool.", required=False)
        parser.add_argument("--verbose", "-v", help="Show verbose output.", required=False, action="store_true")
        parser.add_argument("--update-templates", "-ut", help="Update nuclei-templates to latest released version.", required=False)
        self.args = parser.parse_args()

        # python Main.py - u "http://54.179.181.52:8001/contact" - p "http://127.0.0.1:8080" - t CVE-2021-44228.yaml
        # Lỗi: Main.py: error: unrecognized arguments: http://127.0.0.1:8080
        # Note: Tìm hiểu tham số action="store_true" trong hàm add_argument để fix

    def argumentHandling(self):
        config_yaml = {}

        if self.args.target:
            config_yaml['url'] = self.args.target

        if self.args.list:
            config_yaml['list'] = self.args.list
        
        if self.args.templates:
            config_yaml['templates'] = self.args.templates
        
        if self.args.it:
            config_yaml['it'] = self.args.it

        if self.args.tag:
            config_yaml['tag'] = self.args.tag

        if self.args.severity:
            config_yaml['severity'] = self.args.severity

        if self.args.author:
            config_yaml['author'] = self.args.author

        if self.args.output_file:
            config_yaml['severity'] = self.args.severity
        
        if self.args.include_rr:
            config_yaml['include_rr'] = self.args.include_rr
        
        if self.args.thread:
            config_yaml['thread'] = self.args.thread
        
        if self.args.interactsh_server:
            config_yaml['interactsh_server'] = self.args.interactsh_server
        
        if self.args.timeout:
            config_yaml['timeout'] = self.args.timeout
        
        if self.args.retries:
            config_yaml['retries'] = self.args.retries
        
        if self.args.debug:
            config_yaml['debug'] = self.args.debug
        
        if self.args.debug_req:
            config_yaml['debug_req'] = self.args.debug_req
        
        if self.args.debug_resp:
            config_yaml['debug_resp'] = self.args.debug_resp
        
        if self.args.proxy:
            config_yaml['proxy'] = self.args.proxy
        
        if self.args.version:
            config_yaml['version'] = self.args.version
        
        if self.args.verbose:
            config_yaml['verbose'] = self.args.verbose
        
        if self.args.update_templates:
            config_yaml['update_templates'] = self.args.update_templates

        with open(r'../config.yaml', 'w') as file:
            documents = yaml.dump(config_yaml, file)

        # Chạy thử lệnh python Main.py -u "http://54.179.181.52:8001/contact" -p -t CVE-2021-44228.yaml
        # Không thấy tạo file config.yaml