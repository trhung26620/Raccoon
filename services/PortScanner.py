import socket
import nmap
from utils.PrinterUtil import Printer


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
        services = []
        for host in allHost:
            ports = nm[host]['tcp'].keys()
            for port in ports:
                state = nm[host]['tcp'][port]['state']
                if state == "open":
                    service = nm[host]['tcp'][port]
                    services.append(service)
        return services

    # return list of open port
    @staticmethod
    def getOpenPort(target):
        openPorts = []
        nm = nmap.PortScanner()
        Printer.printInfo("Scanning for open ports at: " + target + " ... ")
        nm.scan(target, '1-65535')
        ports = nm[target]['tcp'].keys()
        for port in ports:
            state = nm[target]['tcp'][port]['state']
            if state == "open":
                openPorts.append(port)
        return openPorts








