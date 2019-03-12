#!usr/bin/python

template = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CGI 101</title>
</head>
<body>
    <h1>Third CGI Script</h1>
    <hr>
        <p>Hello, CGI world!</p>
        $TABLE$
    <hr>
</body>
</html>
"""


table = """<table border=1>
$ROWS$\t\t</table>"""

rows = ""

for i in range(5):
    row = "\t\t\t<tr>{}\n\t\t\t</tr>\n"
    data = ""
    for j in range(4):
        data += "\n\t\t\t\t<td>{}.{}</td>".format(i, j)
    rows += row.format(data)

res_html = template.replace("$TABLE$", table.replace("$ROWS$", rows))
print(res_html)
