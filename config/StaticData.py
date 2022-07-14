class InteractShStaticValue:
    RegisterApi = "https://interact.sh/register"
    RegisterTimeOut = 30
    PollDataApi = "https://interact.sh/poll?"
    PollDataTimeOut = 5
    interactShPrimaryDomain = "interact.sh"
    maxPollingTime = 3


class DefaultTemplateConfig:
    defaultRedirect = False
    defaultStopAtFirstMatch = False
    defaultScanMode = "batteringram"
    defaultInteractShUrl = ""  # no use of interactSh
    defaultThread = 10
    defaultCookieReuse = False
    defaultMatchersCondition = "or"
    defaultRequestCondition = False


class DefaultRequestFiringConfig:
    defaultTimeout = 10
    allow_redirect = True
    proxy = {}


class DefaultConfigMatcher:
    defaultCondition = "or"
    defaultPart = "body"
    defaultNegative = False
    defaultType = None
    defaultSignature = None


class DefaultConfigExtractor:
    defaultType = None
    defaultSignature = None
    defaultPart = "body"
    defaultInternal = False
    defaultGroup = 0


class Template:
    templatePath = None


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


class HTMLReportGlobal:
    HTMLReportList = []


class Subdomain:
    apiUrl = "https://crt.sh/?q="
    wordListFileName = "testWordlist.txt"
    thread = 40


class Debug:
    DebugInfo = []


class SeverityCounter:
    vulnerableTemplates = []
    infoSeverityCounter = 0
    lowSeverityCounter = 0
    mediumSeverityCounter = 0
    highSeverityCounter = 0


class AboutUs:
    version = "Raccoon version 1.1.0"
    author = "Hung, Dat, Danh, Hoa"
    banner = """
    


    ██████╗  █████╗  ██████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔═══██╗████╗  ██║
    ██████╔╝███████║██║     ██║     ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══██╗██╔══██║██║     ██║     ██║   ██║██║   ██║██║╚██╗██║
    ██║  ██║██║  ██║╚██████╗╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
     Raccoon v1.1.0
     Visit our documentation at https://raccoon-solution.online
     Coded by Hung Tran, Dat Tran, Danh Dao, Hoa Le  
     
     

    """ #Font Name: Slant
