#!usr/bin/python
"""
выполняется на стороне сервера, читает данные формы, выводит разметку HTML
"""

import cgi
import sys
sys.stdout.reconfigure(encoding="utf-8")


form = cgi.FieldStorage()
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
        <h4>Your name is: {name}</h4>
        <h4>Your wear rather: {shoesize}</h4>
        <h4>Your current job: {job}</h4>
        <h4>Your program in: {language}</h4>
        <h4>You also said:</h4>
        <p>{comment}</p>
    <hr>       
</body>
</html>
"""

data = {}
for field in {"name", "shoesize", "job", "language", "comment"}:
    if field not in form:
        data[field] = "(unknown)"
    else:
        if not isinstance(form[field], list):
            data[field] = form[field].value
        else:
            values = [x.value for x in form[field]]
            data[field] = " and ".join(values)
print(template.format(**data))
