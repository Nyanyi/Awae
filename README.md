# Awae

## SQLi
1. Book: https://www.amazon.es/Injection-Attacks-Defense-Justin-Clarke-Salt/dp/1597499633/ref=sr_1_1?dchild=1&qid=1602713963&refinements=p_27%3AJustin+Clarke-Salt&s=books&sr=1-1

2. https://portswigger.net/web-security/sql-injection

3. https://www.pentesterlab.com/exercises/from_sqli_to_shell/course

4. https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection

5. http://pentestmonkey.net/category/cheat-sheet/sql-injection

6. https://sqlwiki.netspi.com/

### Discovery SQLi

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
