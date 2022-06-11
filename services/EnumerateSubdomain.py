from bs4 import BeautifulSoup
import requests
from utils.FileUtil import FileUtil
from config.StaticData import Subdomain
from concurrent.futures import ThreadPoolExecutor

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
        with ThreadPoolExecutor(max_workers=Subdomain.thread) as executor:
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
    def getFinalSubdomainList(domain):
        wordlist = FileUtil.getWordlistPath()
        subList1 = EnumSubdomain.enumSubdomainWithThirdParty(domain)
        subList2 = EnumSubdomain.enumSubdomainWithWordList(domain, wordlist)
        subList = list(dict.fromkeys(subList1 + subList2))
        # subList = list(dict.fromkeys(subList1))
        return subList




