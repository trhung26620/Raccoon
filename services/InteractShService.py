import json
import uuid, base64
import time
from Crypto.Cipher import PKCS1_OAEP, AES
from Cryptodome.Hash import SHA256
from Crypto.PublicKey import RSA
from termcolor import colored, cprint
import requests
from config.StaticData import InteractShStaticValue
import urllib3


class InteractSh:
    def __init__(self, key, secret, subDomain, httpProxy):
        self.key = RSA.generate(2048)
        self.secret = str(uuid.uuid4())
        self.subDomain = subDomain
        self.httpProxy = httpProxy
        urllib3.disable_warnings()      # disable TSL/SSL warning

    # return url format: randomStr.interact.sh
    def registerInteractShServer(self):
        publicKey = self.key.public_key().exportKey
        correlation = self.subDomain[:20]

        data = {
            "public-key": publicKey,
            "secret-key": self.secret,
            "correlation-id": correlation
        }

        session = requests.Session()
        session.proxies.update(self.httpProxy)
        session.verify = False
        session.allow_redirects = True
        registerCall = session.post(url=InteractShStaticValue.RegisterApi, json=data, timeout=InteractShStaticValue.RegisterTimeOut)
        registerSuccessSignature = "registration successful"

        if registerSuccessSignature in registerCall.content.decode():
            interactUrl = self.subDomain + "." + InteractShStaticValue.interactShPrimaryDomain
            cprint("\n[*] Registered interactSh successfully", "blue")
            # self.util.saveResult("\n[*] Registered interactSh successfully")  # implement later
            cprint("    [•] Interact URL: " + interactUrl, "cyan")
            # self.util.saveResult("    [•] Interact URL: " + interact_url)     # implement later
        else:
            cprint("\n[*] Error while registering interactSh", "red")
            # self.util.saveResult("\n[*] Error while registering interactSh")  # implement later
            exit()
        return interactUrl

    def pollDataFromWeb(self):
        correlation = self.subDomain[:20]
        responseJson = None
        queryStr = "id={}&secret={}".format(correlation, self.secret)

        session = requests.Session()
        session.proxies.update(self.httpProxy)
        session.verify = False
        session.allow_redirects = True
        maxPollingTime = InteractShStaticValue.maxPollingTime
        cprint("\n[*] Waiting for a response(up to " + str(2 * maxPollingTime) + " seconds)...\n", "yellow")
        # self.util.saveResult("\n[*] Waiting for a response(up to " + str(2 * maxPollingTime) + " seconds)...\n")  # implement later
        isError = False
        for second in range(maxPollingTime):
            isError = False
            time.sleep(2)
            try:
                fetchData = session.get(url=InteractShStaticValue.PollDataApi + queryStr, timeout=InteractShStaticValue.PollDataTimeOut)
            except TimeoutError:
                cprint("\n[*] Interactsh not responding", "red")
                # self.util.saveResult("\n[*] InteractSh not responding")        # implement later
                if second < maxPollingTime - 1:
                    cprint("\n[*] Trying again...", "yellow")
                    # self.util.saveResult("\n[*] Trying again...")         # implement later
                    isError = True
                    continue
            responseJson = fetchData.json()

            if responseJson is None:
                # print("[Debug - InteractSh-Service] No Response ")
                isError = True
                break
            # else:
            #     print("[Debug - InteractSh-Service] Response: " + str(responseJson))

            if "error" in responseJson:
                isError = True
                cprint("\nError when polling data: " + responseJson["error"], "red")
                break

            if responseJson["data"]:
                break
        if not isError:
            data = responseJson["data"]
            aesKey = responseJson["aes_key"]
            return data, aesKey
        else:
            return None, None

    # Decrypt key from interactSh server
    def decryptAESKey(self, aes_Key):
        privateKey = RSA.import_key(self.key.export_key())
        # print("[Debug - InteractSh Service] Private key: " + str(self.key.export_key()))
        rsaKey = PKCS1_OAEP.new(key=privateKey, hashAlgo=SHA256)
        rawAESKey = base64.b64decode(aes_Key)
        decryptAESKey = rsaKey.decrypt(rawAESKey)
        # print("[Debug - InteractSh Service] Decrypted AES key: " + str(decryptAESKey))
        return base64.b64encode(decryptAESKey).decode()

    # Decrypt message from interactSh server (return plaintext)
    @staticmethod
    def decryptMessage(aesKey, dataList):
        if dataList:
            listPlainText = list()
            for data in dataList:
                iv = base64.b64decode(data)[:16]
                key = base64.b64decode(aesKey)
                cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
                plainText = cipher.decrypt(base64.b64decode(data)[16:])
                listPlainText.append(json.loads(plainText))
            return listPlainText
        return None

