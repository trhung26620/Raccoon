class InteractShStaticValue:
    RegisterApi = "https://interact.sh/register"
    RegisterTimeOut = 30
    PollDataApi = "https://interact.sh/poll?"
    PollDataTimeOut = 5
    interactShPrimaryDomain = "interact.sh"
    maxPollingTime = 10

class DefaultTemplateConfig:
    defaultRedirect = False
    defaultStopAtFirstMatch = False
    defaultScanMode = "batteringram"
    defaultInteractShUrl = ""  # no use of interactSh
    defaultThread = 10
    defaultCookieReuse = False
    defaultMatchersCondition = "or"

class DefaultRequestFiringConfig:
    defaultTimeout = 5
    allow_redirect = True
    proxy = {}

class DefaultConfigMatcher:
    defaultCondition = "or"
    defaultPart = "all"
    defaultNegative = False
    defaultType = None
    defaultSignature = None

class DefaultConfigExtractor:
    defaultType = None
    defaultSignature = None
    defaultPart = "all"
    defaultInternal = False
    defaultGroup = None

class Parttern:
    interactUrl = "{{interactsh-url}}"
    baseUrl = "{{BaseURL}}"
    rootUrl = "{{RootURL}}"
    hostName = "{{Hostname}}"
    host = "{{Host}}"
    port = "{{Port}}"
    fullPath = "{{FullPath}}"
    path = "{{Path}}"
    scheme = "{{Scheme}}"

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
