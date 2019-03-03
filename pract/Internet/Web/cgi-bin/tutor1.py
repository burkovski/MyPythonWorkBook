#!usr/bin/python

template = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CGI 101</title>
</head>
<body>
    <h1>Second CGI Script</h1>
    <hr>
        <p>Hello, CGI world!</p>
        <img src="../ppsmall.gif" border=1 alt=[image]>
    <hr>
</body>
</html>
"""

print(template)
