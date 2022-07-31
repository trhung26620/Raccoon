from bs4 import BeautifulSoup
import requests
from utils.FileUtil import FileUtil
from config.StaticData import Subdomain
from concurrent.futures import ThreadPoolExecutor
import string
import random
from termcolor import colored, cprint
import os

class EnumSubdomain:
    @staticmethod
    def enumSubdomainWithThirdParty(domain):
        target = Subdomain.apiUrl + domain
        subList = list()
        try:
            r = requests.get(target)
            data = r.text
        except:
            return []
        soup = BeautifulSoup(data, 'html.parser')
        resultList = soup.find_all("tr")
        for x in resultList:
            soup = BeautifulSoup(str(x), 'html.parser')
            tdList = soup.find_all("td")
            if len(tdList) == 7 and "<br/>" not in str(tdList[5]):
                subList.append(tdList[5].get_text())
        return subList

    @staticmethod
    def isAliveSubdomain(domain_name, subdomain):
        # subList = list()
        # PROXY = {
        #     "http": "http://172.30.176.1:8080",
        #     "https": "http://172.30.176.1:8080",
        # }
        # session = requests.Session()
        # session.proxies.update(PROXY)
        # session.verify = False
        # with open(subdomainFile,'r') as file:
        #     name = file.read()
        #     sub_domnames = name.splitlines()
        # for subdomain in sub_domnames:
            # url = f"https://{subdomain}.{domain_name}"
        url1 = f"https://{subdomain}.{domain_name}"
        url2 = f"http://{subdomain}.{domain_name}"
        try:
            requests.get(url1)
            # subList.append(subdomain+"."+domain_name)
            return subdomain+"."+domain_name
        except:
            pass
        try:
            requests.get(url2)
            # subList.append(subdomain+"."+domain_name)
            return subdomain+"."+domain_name
        except:
            pass
        return None
            # return None
        # return subList

    @staticmethod
    def enumSubdomainWithWordList(domain_name, subdomainFile):
        subList = list()
        threads = []
        with open(subdomainFile,'r') as file:
            name = file.read()
            sub_domnames = name.splitlines()
        with ThreadPoolExecutor(max_workers=int(Subdomain.thread)) as executor:
            for subdomain in sub_domnames:
                threads.append(executor.submit(EnumSubdomain.isAliveSubdomain, domain_name, subdomain))
        futureList = list()
        for future in threads:
            futureList.append(future.result())
        for data in futureList:
            if data:
                subList.append(data)
        return subList

    @staticmethod
    def exportSubdomainFormatTxt(subList):
        subList = ['https://' + i for i in subList]
        letters = string.ascii_lowercase
        fileName = "domains_" + ''.join(random.choice(letters) for i in range(5)) + ".txt"
        f = open(Subdomain.defaultFilePathWithTxtFormat + fileName, "w")
        f.write("\n".join(subList))
        f.close
        return fileName

    @staticmethod
    def getFinalSubdomainList(domain):
        wordlist = FileUtil.getWordlistPath()
        subList1 = EnumSubdomain.enumSubdomainWithThirdParty(domain)
        subList2 = EnumSubdomain.enumSubdomainWithWordList(domain, wordlist)
        subList = list(dict.fromkeys(subList1 + subList2))
        # subList = list(dict.fromkeys(subList1))
        fileName = EnumSubdomain.exportSubdomainFormatTxt(subList)
        cprint("[Info] - Export Domain File to: " + os.path.abspath(Subdomain.defaultFilePathWithTxtFormat + fileName), "yellow")
        return subList




