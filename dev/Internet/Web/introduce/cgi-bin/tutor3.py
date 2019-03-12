#!usr/bin/python
"""
выполняется на стороне сервера, читает данные формы, выводит разметку HTML;
url=http://server-name/cgi-bin/tutor3.py
"""

import cgi
import sys

sys.stdout.reconfigure(encoding="utf-8")
form = cgi.FieldStorage()       # Извлечь данные из формы
template = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CGI 101</title>
</head>
<body>
    <h1>Greetings</h1>
    <hr>
        <p>{user}</p> 
    <hr>       
</body>
</html>"""

if 'user' not in form:
    print(template.format(user="Who are you?"))
else:
    print(template.format(user="Hello, {}!".format(form["user"].value)))
