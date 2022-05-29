from bs4 import BeautifulSoup
import requests
from utils.FileUtil import FileUtil
from config.StaticData import Subdomain

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
    def enumSubdomainWithWordList(domain_name, subdomainFile):
        subList = list()
        with open(subdomainFile,'r') as file:
            name = file.read()
            sub_domnames = name.splitlines()
        for subdomain in sub_domnames:
            url = f"https://{subdomain}.{domain_name}"
            try:
                requests.get(url)
                subList.append(subdomain+domain_name)
            except:
                pass
        return subList

    @staticmethod
    def getFinalSubdomainList(domain):
        wordlist = FileUtil.getWordlistPath()
        subList1 = EnumSubdomain.enumSubdomainWithThirdParty(domain)
        subList2 = EnumSubdomain.enumSubdomainWithWordList(domain, wordlist)
        subList = list(dict.fromkeys(subList1 + subList2))
        return subList