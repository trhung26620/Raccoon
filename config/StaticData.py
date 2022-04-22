class InteractShStaticValue:
    RegisterApi = "https://interact.sh/register"
    RegisterTimeOut = 30
    PollDataApi = "https://interact.sh/poll?"
    PollDataTimeOut = 5
    interactShPrimaryDomain = "interact.sh"
    maxPollingTime = 10


class DefaultTemplateConfig:
    defaultRedirect = True
    defaultThread = 10
    defaultStopAtFirstMatch = False

class DefaultRequestFiringConfig:
    defaultTimeout = 5
    allow_redirect = True
    proxy = None

class AboutUs:
    version = "PowerScanner version 1.1.0"
    author = "Hung, Dat, Danh, Hoa"
    banner = """
    
    
    
        ____                          _____                                 
       / __ \____ _      _____  _____/ ___/_________ _____  ____  ___  _____
      / /_/ / __ \ | /| / / _ \/ ___/\__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
     / ____/ /_/ / |/ |/ /  __/ /   ___/ / /__/ /_/ / / / / / / /  __/ /    
    /_/    \____/|__/|__/\___/_/   /____/\___/\__,_/_/ /_/_/ /_/\___/_/     
                                                                        
     PowerScanner v1.1.0
     Coded by Hung, Dat, Danh, Hoa  
     
     

    """ #Font Name: Slant