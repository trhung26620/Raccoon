from config.StaticData import AboutUs
from colorama import Fore, Back, Style
import colorama

class DisplayUtil:
    colorama.init(autoreset=True)
    @staticmethod
    def displayBanner():
        print(f"{Style.BRIGHT}{Fore.MAGENTA}{AboutUs.banner}")
