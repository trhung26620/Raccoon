import nmap
from utils.PrinterUtil import Printer


class TestMain:

    nm = nmap.PortScanner()
    target = "103.90.225.135"
    Printer.printInfo("Scanning services at target: " + str(target) + "..... ")
    nm.scan(target, '1-65535')
    allHost = nm.all_hosts()
    services = []

    for host in allHost:
        ports = nm[host]['tcp'].keys()
        for port in ports:
            state = nm[host]['tcp'][port]['state']
            if state == "open":
                print("Running service: " + str(nm[host]['tcp'][port]))

