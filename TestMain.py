from termcolor import colored, cprint
from datetime import datetime


class TestMain:
    info = "something need to print"
    cve = colored("CVE-2021-44228", "blue", attrs=['bold'])
    nowStr = str(datetime.now())
    colorNow = colored(nowStr, "magenta", attrs=['bold'])
    pattern = "[" + colorNow + "]" + " [" + cve + "] " + info
    print(pattern)
    errortag = colored("[ERROR]", "red", attrs=["bold", "dark"])
    print(errortag)