# Análisis de código

## Introducción

1. Aprender cuales son las vulnerabilidades más comunes para la aplicación objetivo. Las vulnerabilidades web son diferentes a las vulnerabilidades de un thin client
2. Aprender las firmas de esas vulnerabilidades, no es lo mismo un sqli que un xss
3. Obtener información sobre el lenguaje, las librerías, el framework etc
4. Definir el propósito y contexto de la aplicación
5. Debilidad vs Vulnerabilidad
6. Palabras clave: 
   1. Source: Código que permite que haya una vulnerabilida
   2. Sink: Donde sucede la vulnerabilidad

```
Take command injection vulnerabilities, for example. A “source” in this case could be a function that takes in user input. Whereas the “sink” would be functions that execute system commands. If the untrusted user input can get from “source” to “sink” without proper sanitization or validation, there is a command injection vulnerability.

Many common vulnerabilities can be identified by tracking this “data flow” from appropriate sources to corresponding sinks.
```

### Sast y Dast

**Sast**: Static Analysis Security Testing (no hay ejecución)

**Dast**:  Los DAST examinan solo las respuestas del sistema a una serie de pruebas diseñadas para resaltar vulnerabilidades. Son, en definitiva, un escáner de vulnerabilidades.

Seguridad de aplicaciones dinámicas (DAST), proporciona una perspectiva externa de la aplicación antes del funcionamiento; Estas pruebas, también conocidas como ” *pruebas de caja negra* “, prueban las interfaces expuestas de una aplicación en ejecución en busca de vulnerabilidades y fallas, generalmente en aplicaciones web.

### Idea

Es importante acordarse que la revisión de código no es solo sobre la estructura de código sino también sobre los datos.

## Fases de la revisión de código

### Fase 1 - Preparación y obtención de información

1. Definición general de los principales riesgos. 
2. Determinar la facilidad de exposición: ¿esta expuesta a Internet?
3. Definir el  propósito de la aplicación y sus prioridades. Eso nos ayudara a determinar que funciones, código, es mas critico
4. Conocer la estructura del código
5. Obtener detalles sobre el Lenguaje de programación, framework, etc
6. Documentación

```
The design and the
architecture of the application must be understood thoroughly to analyze vulnerable areas that can lead to security
breaches in the application
```

### Fase 2 - Modelado de amenazas

#### Modelado de amenazas

Realizar una modelado de amenazas de la aplicación para priorizar que partes han de ser revisadas y cuales no.

```
A security review of the application should uncover common security bugs as well as the issues specifc to business
logic of the application. In order to efectively review a body of code it is important that the reviewers understand
the business purpose of the application and the critical business impacts. The reviewers should understand the attack
surface, identify the diferent threat agents and their motivations, and how they could potentially attack the application.
```

#### Descomposición de la aplicacion

El primer paso en el proceso de modelado de amenazas tiene que ver con comprender la aplicación y cómo interactúa con agentes externas. Esto implica crear casos de uso para comprender cómo se usa la aplicación, identificar puntos de entrada para ver dónde un atacante potencial podría interactuar con la aplicación, identificar a áreas en los que el atacante estaría interesado (funcionalidades) e identificar los niveles de confianza que representan los derechos de acceso que la aplicación otorgará a entidades externas.

En resumen, obtener esta información:

- External depencias
- Entry points
- Funcionalidades interesantes
- Determinar la superficie de ataque
- Autorizaciones
- Data flow
- Transacciones

##### Determinar posibles las amenazas

- Spoofing
- Tampering
- Reputacion
- Information disclousure
- Denial of service
- elevation of privilege
- Posibles escenarios de ataque

```
All security is in context of what we are trying to secure. Recommending military standard security mechanisms on
an application that vends apples would be overkill and out of context. What type of data is being manipulated or
processed, and what would the damage to the company be if this data was compromised? Context is the “Holy Grail”
of secure code inspection and risk assessment
```

##### Determinar impactos y probabilidad

- Damage
- Reproducibilidad
- Explotabilidad
- Usuarios afectados
- Facilidad de descubrimiento

```
Riesgo = likelihood x impact
```

### Fase 3 - Documentación

Documentar todo lo que hayas obtenido

### Fase 4 - Primeras acciones a realizar

1. Búsqueda de strings, keywoards, code patterns (api keys, encryptions keys, database passwords) buscando key, secret, passwords en hex o base64
2. Búsqueda de firmas de vulnerabilidades (cómo consultas SELECT)
3. Funciones "peligrosas"
   - Sobretodo las que tengan entrada del usuario
   - system, eval(), input(), etc
   - Mirar las especificas de cada lenguaje
4. Comentarios del desarrollador
5. Ficheros de configuración
6. Endpoints abandonados o en desarrollo
7. Dependecias outdated
8. Falta de checks de seguridad en los "user input"
9. Funciones controladas por el usuario
10. Debilidades criptograficas (ecb, md4, md5)

### Fase 5 - Bajar al barro

1. User input
   - http request
   - http parameters
   - database entries
   - file uploads
2. Funciones:
   - Funciones de autorizacion
   - Funciones de autenticacion
   - Logicas
   - Bussines
   - Configuración

```
It is said that a review goes best when conducted on less than 400 lines of code at a time. You should do a proper and slow review, however, don’t spend on it more than 90 minutes 
```

## Estrategias

### Ideas basicas

1. Analizar los user input
2. Analizar las funciones, como se relacionan entre si
3. Escribir el esqueleto de las funciones, los input etc
4. Comprobar como llegan las variables y que protecciones se realizan a las funciones
5. Debilidades vs vulnerabilidades
6. Hay código danger-> como llegan las variables-> son filtradas?-> es alcanzable por el usuario
7. Comprobar siempre los filtrados, como están hecho, y en que momentos se están realizando
8. una vez están organizadas las funciones, se pueden implementar las siguientes revisiones:
   1. Revisar de arriba a abajo, de izquierda a derecha (revisar todo)
      1. mucho tiempo
      2. cubres todo
      3. no sigues el flujo de un usuario
   2. Empezar por una funcion con entrada de usuario y seguir el flujo (arriba a abajo)
   3. Empezar por una funcion abajo y seguir hacia arriba
   4. Buscando palabras claves (system, eval, select...)
   5. Buscar funciones criticas, como password reset

### Trace Malicious Input

```
You start at an entry point to the system, where user-malleable information
can come in. You then trace the flow of code forward, performing limited data flow
analysis. You keep a set of possible "bad" inputs in the back of your mind as you read
the code and try to trace down anything that looks like a potential security issue. This 
technique is an effective way to analyze code, but it requires some experience so that
you know which functions to trace into.

Start point Data entry points
End point Security vulnerabilities (open-ended)
Tracing method Forward, control-flow sensitive, data-flow sensitive
Goal Discover security problems that can be caused by malicious
input.
```

### Candidate Point Strategies

```
Candidate point (CP) strategies are one of the fastest ways of identifying the most
common classes of vulnerabilities. These strategies focus on identifying idioms and
structured code patterns commonly associated with software vulnerabilities. The
reviewer can then back-trace from these candidate points to find pathways allowing
access from untrusted input. The simplicity of this approach makes candidate point
strategies the basis for most automated code analysis. Of course, the disadvantage is
that these strategies don't encourage a strong understanding of the code and ignore
vulnerabilities that don't fit the rather limited candidate point definitions.

Start point Potential vulnerabilities
End point Any form of user-malleable input
Tracing method Backward, control-flow sensitive, data-flow sensitive
Goal: Given a list of potential vulnerabilities, determine whether they
are exploitable
```

## Owasp

### System development cycle

```
All security code reviews are a combination of human efort and technology support. At one end of the spectrum is an inexperienced person with a text editor. At the other end of the scale is an expert security team with advanced static analysis (SAST) tools. Unfortunately, it takes a fairly serious level of expertise to use the current application security tools efectively. They also don’t understand dynamic data fow or business logic. SAST tools are great for coverage and setting a minimum baseline.

Tools can be used to perform this task but they always need human verifcation. They do not understand context, which is the keystone of security code review. Tools are good at assessing large amounts of code and pointing out possible issues, but a person needs to verify every result to determine if it is a real issue, if it is actually exploitable, and calculate the risk to the enterprise. Human reviewers are also necessary to fll in for the signifcant blind spots, which automated tools, simply cannot check.

The term “360 review” refers to an approach in which the results of a source code review are used to plan and execute a penetration test, and the results of the penetration test are, in turn, used to inform additional source code review.

There are various reasons why security faws manifest in the application, like a lack of input validation or parameter mishandling. In the process of a code review the exact root cause of faws are exposed and the complete data fow is traced. The term ‘source to sink analysis’ means to determine all possible inputs to the application (source) and how they are being processed by it (sink). A sink could be an insecure code pattern like a dynamic SQL query, a log writer, or a response to a client device. 
```

#### Checklist:

- Data validation - Data flow
- Autenticacion
- session management
- authorizacion
- cryptografia
- manejo de errores
- logging
- configuraciones de seguridad
- arquitectura de red
- FIcheros de configuracion y data stores

#### Motivos de errores:

- Código inseguro
- Diseño 
- configuración

#### Determina salvaguardas

- Vulnerabilidades no mitigables
- Parcialmente mitigables
- Totalmente mitigables

### Vulnerabilidades

#### Injection

- Sqli

  - Using string concatenation to generate a SQL statement is very common in legacy applications where developers were not considering security. The issue is this coding technique does not tell the parser which part of the statement is code and which part is data. In situations where user input is concatenated into the SQL statement, an attacker can modify the SQL statement by adding SQL code to the input data.

    - SELECT
    - Concatenaciones

    ```
    String custQuery = SELECT custName, address1 FROM cust_table WHERE custID= ‘“ + request.GetParameter(“id”) + ““
    ```

  - EXEC, EXECUTE

- Json injection

  - javascript
  - Funciones eval()

- CSP

  - Fallos de misconfiguration
  - politicas demasiado permisivas
  - Uso de http headers
  - 

- Input validation

  - “Don’t trust user input”
  - “Golden Rule: All external input, no matter what it is, will be examined and validated.
  - Ensure all input that can (and will) be modifed by a malicious user such as HTTP headers, input felds, hidden felds, drop down lists, and other web components are properly validated. 
  - Ensure that all felds, cookies, http headers/bodies, and form felds are validated. 

#### Broken autenticacion y session management

- Login
  -  Ensure the login page is only available over TLS.
  -  usernames/user-ids are case insensitive.
  -  Ensure failure messages for invalid usernames or passwords do not leak information. 
  -  Cryptografia
- Funcionalidad de olvido de passswords
- Captcha
- out band communication
- gestion de la sesion
- session logout
- session hijacking
- session fixation
- sesion elevation

#### XSS

- insecure direct object
- security misconfigurations
- sensitive data exposure
- acces control
- csrf
- utilizacion de componentes con debilidades
- redirect

## Recursos

1. https://medium.com/palantir/code-review-best-practices-19e02780015f 
2. https://blog.shiftleft.io/how-to-review-code-for-vulnerabilities-1d017c21a695
3. https://owasp.org/www-pdf-archive/OWASP_Code_Review_Guide_v2.pdf (https://owasp.org/www-pdf-archive/OWASP_Code_Review_Guide-V1_1.pdf)
4. https://medium.com/@same7mabrouk/the-checklist-of-my-code-review-18cc6f6fb5b3
5. https://google.github.io/eng-practices/review/reviewer/
6. https://medium.com/swlh/code-review-101-2e3f7c142c7e
7. https://pentesterlab.com/badges/codereview
8. https://securitylab.github.com/tools/codeql
9. https://www.atlassian.com/agile/software-development/code-reviews
10.https://www.amazon.es/Art-Software-Security-Assessment-Vulnerabilities/dp/0321444426


