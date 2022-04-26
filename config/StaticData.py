class InteractShStaticValue:
    RegisterApi = "https://interact.sh/register"
    RegisterTimeOut = 30
    PollDataApi = "https://interact.sh/poll?"
    PollDataTimeOut = 5
    interactShPrimaryDomain = "interact.sh"
    maxPollingTime = 10


class DefaultTemplateConfig:
    defaultRedirect = True
    defaultStopAtFirstMatch = False
    defaultScanMode = "batteringram"
    defaultInteractShUrl = ""  # no use of interactSh
    defaultThread = 10
    defaultCookieReuse = False

class DefaultRequestFiringConfig:
    defaultTimeout = 5
    allow_redirect = True
    proxy = {}

class AboutUs:
    version = "Racoon version 1.1.0"
    author = "Hung, Dat, Danh, Hoa"
    banner = """
    

    ██████╗  █████╗  ██████╗ ██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔═══██╗████╗  ██║
    ██████╔╝███████║██║     ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══██╗██╔══██║██║     ██║   ██║██║   ██║██║╚██╗██║
    ██║  ██║██║  ██║╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
     Racoon v1.1.0
     Coded by Hung, Dat, Danh, Hoa  
     
     

    """ #Font Name: Slant
