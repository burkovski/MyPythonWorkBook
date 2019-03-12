#!/usr/bin/python
"""
выполняется на сервере, выводит разметку HTML для создания новой страницы;
url=http://localhost/cgi-bin/tutor0.py
"""

tmp = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CGI 101</title>
</head>
<body>
    <h1>A First CGI Script</h1>
    <p>Hello, CGI world!</p>
</body>
</html>"""

print(tmp)
