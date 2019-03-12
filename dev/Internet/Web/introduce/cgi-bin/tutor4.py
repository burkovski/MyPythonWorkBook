#!usr/bin/python
"""
выполняется на стороне сервера, читает данные формы, выводит разметку HTML;
URL http://server-name/cgi-bin/tutor4.py
"""

import cgi
import sys
sys.stdout.reconfigure(encoding="utf-8")


sys.stderr = sys.stdout         # Для вывода сообщений об ошибках в бразуере
form = cgi.FieldStorage()       # Извелчь данные из формы
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
        <h4>{0}</h4>
        <h4>{1}</h4>
        <h4>{2}</h4>
    <hr>       
</body>
</html>"""


if "user" not in form:
    line1 = "Who are you?"
else:
    line1 = "Hello, {}!".format(form["user"].value)

line2 = "You're talking to a {} server.".format(sys.platform)

if "age" not in form:
    line3 = "NAN"
else:
    try:
        age = int(form["age"].value)
        line3 = "Your age is {}, your age squared is {}.".format(age, age ** 2)
    except Exception:
        line3 = "Sorry, I can't compute {}.".format(form["age"].value)

print(template.format(line1, line2, line3))
