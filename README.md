```
    ██████╗  █████╗  ██████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔═══██╗████╗  ██║
    ██████╔╝███████║██║     ██║     ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══██╗██╔══██║██║     ██║     ██║   ██║██║   ██║██║╚██╗██║
    ██║  ██║██║  ██║╚██████╗╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
```

Raccoon is based on the perception of using YAML template file as the input for sent request, receive and process data from response. One of the main strength of our tool is customizable template. A knowledge user can create their own template suitable with their need. Those template are written by YAML because this language has a simple and clean syntax and very human-readable.

## Install:

**Our tool running under python 3. Make sure you install python version 3 first.**

Clone Raccoon from github.
```
git clone https://github.com/trhung26620/Raccoon.git
```

Clone Raccoon template from github.
```
git clone https://github.com/trhung26620/Raccoon-Template
```

We prepared a file named "requirement.txt" in Raccoon directory contains all the libs need to be installed when using Raccoon.

### Linux
```
pip3 install -r requirement.txt
```

### Windows
```
pip install -r .\requirement.txt
```

Normally the template folder can be cloned anywhere but we suggest you clone this folder in the Raccoon folder to keep the code in sync. In case you want to clone the Template folder to another location, each template will have different fields, if in the template, you need to take wordlist as a parameter, you need to change the path to match your template directory. 

![raccoon-example-1](https://i.imgur.com/CLL0hRD.png)

## Usage:

In current directory, run: python3 Raccoon.py -h will list available options in Raccoon.

```
usage: Raccoon.py [-h] [--gathering] [--target TARGET] [--list LIST] [--templates TEMPLATES] [--it IT] [--tag TAG]
                  [--severity SEVERITY] [--author AUTHOR] [--output-file OUTPUT_FILE] [--thread THREAD]
                  [--interactsh-server INTERACTSH_SERVER] [--timeout TIMEOUT] [--retries RETRIES] [--debug] [--debug-req]
                  [--debug-resp] [--proxy PROXY] [--version] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --gathering, -g       Raccoon will gather information about the target like subdomain, port, services,...
  --target TARGET, -u TARGET
                        Specify a URL to scan.
  --list LIST, -l LIST  Specify path to file containing a list of target URLs to scan (one per line)
  --templates TEMPLATES, -t TEMPLATES
                        Template or template directory paths to include in the scan
  --it IT               Specify templates based on IDs. (e.g. CVE-2021-44228,iis-shortname)
  --tag TAG             Specify templates based on tags. (e.g. cve,fuzz).
  --severity SEVERITY, -s SEVERITY
                        Specify templates based on severities. Possible values: info, low, medium, high, critical.
  --author AUTHOR, -a AUTHOR
                        Execute templates that are (co-)created by the specified authors.
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Specify file path to write info and result during scanning to a file.
  --thread THREAD, -T THREAD
                        Max number of concurrent HTTP(s) requests (default 10)
  --interactsh-server INTERACTSH_SERVER, -is INTERACTSH_SERVER
                        Specify an interactsh server url for self-hosted instance. (Warning: We can not analyze or parse result
                        with this option)
  --timeout TIMEOUT     Time to wait in seconds before timeout (default 10).
  --retries RETRIES     Number of times to retry a failed request (default 0).
  --debug               Show all requests and responses.
  --debug-req           Show all sent requests.
  --debug-resp          Show all received responses.
  --proxy PROXY, -p PROXY
                        Use a proxy to connect to the target URL (e.g. "http://127.0.0.1:8080").
  --version             Show the version of tool.
  --verbose, -v         Show verbose output.
```


Common arguments:

```
-u : Specify target url
-t : Specify a single template or a template's folder
```

Example: 

### Linux
```
python3 Raccoon.py -u http://demo.raccoon-solution.online/ -t Raccoon-Template/CVE/CVE-2021-44228.yaml
```

### Windows
```
python Raccoon.py -u http://demo.raccoon-solution.online/ -t .\Raccoon-Template\CVE\CVE-2021-44228.yaml
```
![raccoon-example-2](https://i.imgur.com/pmwRcQb.png)

```
-p : Specify a proxy address to observe the details of sending and receiving requests

```
Example:

### Linux 
```
python3 Raccoon.py -u http://demo.raccoon-solution.online/ -t Raccoon-Template/CVE/CVE-2021-44228.yaml -p http://127.0.0.1:8080
```

### Windows 
```
python Raccoon.py -u http://demo.raccoon-solution.online/ -t .\Raccoon-Template\CVE\CVE-2021-44228.yaml -p http://127.0.0.1:8080
```

![raccoon-example-3](https://i.imgur.com/6AN7AEL.png)

## For more infomation, please visit our website: 
<a href="https://raccoon-solution.online"> raccoon-solution.online </a>

## Create your own template by following our guide: 
<a href="https://raccoon-solution.online/templateGuide"> raccoon-solution.online/templateGuide </a>