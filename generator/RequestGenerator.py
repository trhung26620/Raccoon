import sys
from operator import mod
import os, yaml
from urllib.parse import urlparse, parse_qs
from re import template
from pathlib import Path
sys.path.append('../')
from utils.TemplateUtil import TemplateUtil
from utils.ConfigUtil import ConfigUtil
from models.Url import Url
from models.Header import Header
from models.Body import Body
from models.Request import Request
import re
# import json


class RequestGenerator:
    @staticmethod
    def replace_parameter(templateData):
        dict_of_request = dict()
        list_of_components_url = RequestGenerator.detached_of_url()
        for component in list_of_components_url:
            list_of_request = []
            urlPattern = {
                '{{BaseURL}}': component['baseUrl'],
                '{{RootURL}}': component['rootUrl'],
                '{{Hostname}}': component['hostname'],
                '{{Host}}': component['host'],
                '{{Port}}': str(component['port']),
                '{{FullPath}}': component['fullPath'],
                '{{Path}}': component['path'],
                '{{Scheme}}': component['scheme']
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
                'path': os.path.split(url.path)[0],
                'scheme': url.scheme,
            }
            list_of_components_url.append(components_url)
        return list_of_components_url

    # Hàm này sẽ nhận một cấu trúc request đầy đủ người dùng cung cấp, sau đó phân tích từng thành phần trong request và trả về giá trị như header, url, query, body, method,...
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
            url = schema + "://" + host + path
        else:
            print("Something went wrong with schema, host or path")
            exit()

        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)

        headerDict = dict()

        for line in reqHeader.split("\n"):
            if not line.startswith("POST") and not line.startswith("GET") and not line.startswith("PUT") and not line.startswith("DELETE"):
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
            reqObjectList = []
            for req in reqList:
                dataReq = RequestGenerator.analystRequest(req, baseUrl)
                if dataReq:
                    url = Url(dataReq["schema"], dataReq["method"], dataReq["host"], dataReq["path"], dataReq["paramPath"], dataReq["url"])
                    header = Header(dataReq["headers"])
                    body = Body(dataReq["body"])
                    request = Request(url, header, body)
                    reqObjectList.append(request)
            reqObjectDict[baseUrl] = reqObjectList
        return reqObjectDict








