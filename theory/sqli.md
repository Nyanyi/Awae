# SQLI

## Discovery SQLi

1.  If a ' is causing the error try to see if \' will result in success message (since the backslash cancels out the single quote in MySQL).
- page.asp?id=1 or 1=1 -- true
- page.asp?id=1' or 1=1 -- true
- page.asp?id=1" or 1=1 -- true
- page.asp?id=1 and 1=2 -- false
- product.asp?id=1/1 -- true
- product.asp?id=1/0 -- false

2.  You can also try if commenting out the ' results in a success message like: %23' or --'. This is because you tell MySQL to explicitly ignore everything after the comment include the extra '.

3.  If a ' is not allowed you can use comparisons between valid and invalid system variables like @@versionz vs @@version or invalid vs valid functions SLEP(5) vs SLEEP(5).

4.  Sometimes your input will end up between () make sure you test input)%23 as well to see if you can break out of these and exploit Union SQLi for example (input) order by 5%23).

5.  If the normal input is just an integer you can try to subtract some amount of it and see if that subtraction works (id=460-5).

6.  Try to see if an even amount of quotes results in a success message (for example 460'' or 460-'') and an uneven amount results in an error (for example 460' or 460-''').

7. Blind - Content Base: In the case of a Content-based Blind SQL Injection attack, the attacker makes different SQL queries that ask the database TRUE or FALSE questions. Then they analyze differences in responses between TRUE and FALSE statements.

8.  Blind - Time Base: In the case of time-based attacks, the attacker makes the database perform a time-intensive operation. If the web site does not return a response immediately, the web application is vulnerable to Blind SQL Injection. A popular time-intensive operation is the sleep operation.
