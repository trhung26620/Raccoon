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


Clone Raccoon from github.
```
git clone https://github.com/trhung26620/Raccoon.git
```
Normally the template folder can be cloned anywhere but we suggest you clone this folder in the Raccoon folder to keep the code in sync. In case you want to clone the Template folder to another location, each template will have different fields, if in the template, you need to take wordlist as a parameter, you need to change the path to match your template directory. 

![raccoon-example-1](https://i.imgur.com/CLL0hRD.png)

## Usage:

In current directory, run: python Raccoon.py -h will list available options in Raccoon.

Common arguments:

```
-u : Specify target url
-t : Specify a single template or a template's folder
```

Example: 
```
python3 Raccoon.py -u http://demo.raccoon-solution.online/ -t Raccoon-Template/CVE/CVE-2021-44228.yaml
```
![raccoon-example-2](https://i.imgur.com/pmwRcQb.png)

```
-p : Specify a proxy address to observe the details of sending and receiving requests

```
Example: 
```
python3 Raccoon.py -u http://demo.raccoon-solution.online/ -t Raccoon-Template/CVE/CVE-2021-44228.yaml -p http://127.0.0.1:8080
```
![raccoon-example-3](https://i.imgur.com/6AN7AEL.png)

## For more infomation, please visit our website: 
<a href="https://raccoon-solution.online"> raccoon-solution.online </a>

## Create your own template by following our guide: 
<a href="https://raccoon-solution.online/templateGuide"> raccoon-solution.online/templateGuide </a>