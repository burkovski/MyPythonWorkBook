#!/usr/bin/python
"""
Отображает содержимое сценария languages.py не выполняя его.
"""

import html
import sys

sys.stdout.reconfigure(encoding="utf-8")


file_name = "cgi-bin/languages.py"
template = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Languages</title>
</head>
<body>
    <h1>Source code: {0}</h1>
    <hr>
    <pre>{1}</pre>
    </hr>
</body>
</html>"""


with open(file_name, encoding="utf-8") as file:
    print(template.format(file_name, html.escape(file.read())))
