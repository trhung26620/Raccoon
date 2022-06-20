

serviceDict1 = {22:  {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '8.2p1 Ubuntu 4ubuntu0.5', 'extrainfo': 'Ubuntu Linux; protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}}
serviceDict2 = {80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:igor_sysoev:nginx'}}
serviceDict3 = {443: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:igor_sysoev:nginx'}}
serviceDict4 = {8001: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache Tomcat', 'version': '9.0.56', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:apache:tomcat:9.0.56'}}

serviceDictList = [serviceDict1, serviceDict2, serviceDict3, serviceDict4]

for index, serviceDict in enumerate(serviceDictList):
    print("Index " + str(index) + " service: " + str(serviceDict))
    for port, service in serviceDict.items():
        print("Port: " + str(port))
        print("State: " + str(service["state"]))

