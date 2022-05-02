import sys
from urllib.parse import urlparse, parse_qs
sys.path.append('../')
from utils.TemplateUtil import TemplateUtil
from utils.ConfigUtil import ConfigUtil
from models.Url import Url
from models.Header import Header
from models.Body import Body
from models.Request import Request
import re
from config.StaticData import Parttern

class RequestGenerator:
    @staticmethod
    def replace_parameter(templateData):
        dict_of_request = dict()
        list_of_components_url = RequestGenerator.detached_of_url()
        for component in list_of_components_url:
            list_of_request = []
            urlPattern = {
                Parttern.baseUrl: component['baseUrl'],
                Parttern.rootUrl: component['rootUrl'],
                Parttern.hostName: component['hostname'],
                Parttern.host: component['host'],
                Parttern.port: str(component['port']),
                Parttern.fullPath: component['fullPath'],
                Parttern.path: component['path'],
                Parttern.scheme: component['scheme']
            }
            for req in templateData['requests'][0]['request']:
                for k, v in urlPattern.items():
                    req = req.replace(k, v)
                list_of_request.append(req)
            dict_of_request[component['baseUrl']] = list_of_request
        return dict_of_request

    @staticmethod
    def detached_of_url():
        list_of_components_url = list()
        for i in ConfigUtil.readConfig()['url']:
            url = urlparse(i)
            components_url = {
                'baseUrl': i,
                'rootUrl': url.scheme + "://" + url.netloc,
                'hostname': url.netloc,
                'host': url.hostname,
                'port': url.port,
                'fullPath': i[len(url.scheme + "://" + url.netloc):],
                # 'path': os.path.split(url.path)[0],
                'path': url.path,
                'scheme': url.scheme,
            }
            list_of_components_url.append(components_url)
        return list_of_components_url

    @staticmethod
    def analystRequest(req, baseUrl):
        method = None
        existBody = False
        url = None
        host = None
        firstLine = req.split('\n')[0]
        if "://" not in baseUrl:
            schema = "http"
        elif baseUrl.split("://")[0] == "http":
            schema = "http"
        elif baseUrl.split("://")[0] == "https":
            schema = "https"
        else:
            # print("Not support schema: " + baseUrl.split("://")[0])
            return
        path = firstLine.strip().split()[1]

        if re.search("^(GET)(\s+)[//]", firstLine):
            method = "GET"
        elif re.search("^(POST)(\s+)[//]", firstLine):
            method = "POST"
        elif re.search("^(PUT)(\s+)[//]", firstLine):
            method = "PUT"
        elif re.search("^(DELETE)(\s+)[//]", firstLine):
            method = "DELETE"
        else:
            print("Only support methods GET|POST|PUT|DELETE")
            exit()

        if len(req.split("\n\n")) > 1 and req.split("\n\n")[1].strip():
            existBody = True

        reqHeader = req.split("\n\n")[0]
        if reqHeader.split("\n")[-1] == "":
            reqHeader = reqHeader[:-1]
        for line in reqHeader.split("\n"):
            if line.lower().startswith("host:"):
                host = line[line.find(':') + 1:].strip()
                break
        if schema and path and host:
            parsed_url = urlparse(baseUrl).path
            if parsed_url=="/":
                parsed_url = ""
            if parsed_url.endswith("/"):
                parsed_url = parsed_url[:-1]
            url = schema + "://" + host + parsed_url + path
        else:
            print("Something went wrong with schema, host or path")
            exit()

        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)

        headerDict = dict()

        for line in reqHeader.split("\n"):
            if not line.startswith("POST") and not line.startswith("GET") and not line.startswith("PUT") and not line.startswith("DELETE"):
                if not line[:5].lower()=="host:":
                    headerDict[line.split(":",1)[0]] = line.split(":", 1)[1].strip()
        reqBody = None
        if existBody:
            lastStringHeader = reqHeader[-20:]
            reqBody = req.split(lastStringHeader + "\n\n")[1][:-1]
        if query:
            url = url[:url.find('?')]
        result = {
            "schema": schema,
            "method": method,
            "host": host,
            "path": path,
            "paramPath": query,
            "headers": headerDict,
            "body": reqBody,
            "url": url
        }
        return result

    @staticmethod
    def generateRequestObject(templateFilePath):
        requestDict = RequestGenerator.replace_parameter(TemplateUtil.readTemplate(templateFilePath))
        reqObjectDict = dict()
        for baseUrl, reqList in requestDict.items():
            count = 1
            reqObjectList = []
            for req in reqList:
                dataReq = RequestGenerator.analystRequest(req, baseUrl)
                if dataReq:
                    url = Url(dataReq["schema"], dataReq["method"], dataReq["host"], dataReq["path"], dataReq["paramPath"], dataReq["url"])
                    header = Header(dataReq["headers"])
                    body = Body(dataReq["body"])
                    request = Request(url, header, body, count)
                    reqObjectList.append(request)
                    count += 1
            reqObjectDict[baseUrl] = reqObjectList
        return reqObjectDict








