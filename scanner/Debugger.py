from utils.ConfigUtil import ConfigUtil
from termcolor import colored, cprint


class Debugger:

    @staticmethod
    def debugCall(info):
        config = ConfigUtil.readConfig()
        debugValue = config["debug"]
        if "debug" == debugValue:
            Debugger.debugOption(info)
        elif "debug_req" == debugValue:
            Debugger.requestDebugOption(info)
        elif "debug_resp" == debugValue:
            Debugger.responseDebugOption(info)

    @staticmethod
    def debugOption(listReqAndResp):
        for debugObject in listReqAndResp:
            for request in debugObject:
                requestHeader = request.header.content
                requestBody = request.body.content
                response = debugObject[request]["response"]
                responseHeader = response.headers
                responseBody = response.text
                cprint("[Debug] - Request header: ", "blue")
                cprint(requestHeader, "yellow")
                cprint("[Debug] - Request body: ", "blue")
                cprint(requestBody, "yellow")
                cprint("[Debug] - Response header: ", "blue")
                cprint(responseHeader, "yellow")
                cprint("[Debug] - Response body: ", "blue")
                cprint(responseBody, "yellow")


    @staticmethod
    def requestDebugOption(listReqAndResp):
        for debugObject in listReqAndResp:
            for request in debugObject:
                requestHeader = request.header.content
                requestBody = request.body.content
                cprint("[Debug] - Request header: ", "blue")
                cprint(requestHeader, "yellow")
                cprint("[Debug] - Debug - Request body: ", "blue")
                cprint(requestBody, "yellow")


    @staticmethod
    def responseDebugOption(listReqAndResp):
        for debugObject in listReqAndResp:
            for request in debugObject:
                response = debugObject[request]["response"]
                responseHeader = response.headers
                responseBody = response.text
                cprint("[Debug] - Response header: ", "blue")
                cprint(responseHeader, "yellow")
                cprint("[Debug] - Response body: ", "blue")
                cprint(responseBody, "yellow")

