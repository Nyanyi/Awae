import requests
from sys import argv
from colorama import Fore, Back, Style

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#Configuration
target="localhost:9090"
url = "http://" + target
payload = {'id':1}
parameters='y'
method='GET'
#proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

#functions
def requests_get_params():
    r = requests.get(url, params=payload, verify=False)
    response(r)

def requests_get_simple():
    r = requests.get(url, verify=False)
    response(r)

def requests_post_params():
    r = requests.post(url, data=payload, verify=False)
    response(r)

def requests_post_simple():
    r = requests.post(url, verify=False)
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

def select_request_get():
    if parameters == 'n':
        request_get_simple()
    else:
        requests_get_params()

def select_request_post():
    if parameterers == 'n':
        requests_post_simple()
    else:
        requests_post_params()

def main():

    if method == 'GET':
        select_request_get()
    else:
        select_request_post()

#start
if __name__== "__main__":
    main()
