import socket
import traceback

import nmap
from utils.PrinterUtil import Printer
import requests
from bs4 import BeautifulSoup


class Scanner:

    # return list of ip
    @staticmethod
    def resolveToIP(domain):
        try:
            data = socket.gethostbyname_ex(domain)
            resolveIPs = data[2]
            return resolveIPs
        except:
            Printer.printError("Can not resolve domain: " + domain)

    # return list of dict contains information about service
    @staticmethod
    def getRunningService(target):
        nm = nmap.PortScanner()
        Printer.printInfo("Scanning services at target: " + str(target) + " .... ")
        nm.scan(target, '1-65535')
        allHost = nm.all_hosts()
        resultList = []
        for host in allHost:
            ports = nm[host]['tcp'].keys()
            for port in ports:
                infoDict = {}
                state = nm[host]['tcp'][port]['state']
                if state == "open":
                    service = nm[host]['tcp'][port]
                    infoDict[port] = service
                    resultList.append(infoDict.copy())
        return resultList

    @staticmethod
    def getWordpressVersion(target):
        try:
            response = requests.get("http://" + target)
            htmlContent = response.text

            if htmlContent is None:
                return None

            soup = BeautifulSoup(htmlContent, "html.parser")
            metaTags = soup.find_all("meta")

            if len(metaTags) == 0:
                return None

            wordpressTag = metaTags[3]

            if wordpressTag is None:
                return None
            return str(wordpressTag['content'])
        except Exception:
            # Printer.printError("Can not detect WordPress version for target: " + target)
            return None









