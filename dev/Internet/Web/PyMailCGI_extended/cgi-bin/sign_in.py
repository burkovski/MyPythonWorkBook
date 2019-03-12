import cgi


form = cgi.FieldStorage()

response = """<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <title>Sign in</title>
    <link rel=icon href="../img/pylove.ico" type="image/x-icon">
</head>
<body>
    <h1>Sign In!</h1>
    <hr>
    <form method="post" action="verify_user.py"><table>
    <tr>
        <th align="left">User name:</th>
        <td><input type="text" name="username" {}></td>
    </tr>
    <tr>
        <th align="left">Password:</th>
        <td><input type="password" name="password"></td>
    </tr>
        <th></th>
        <td colspan="2"><input type="submit" value="Send"></td>
    </tr>
    </table></form>
</body>
"""

username = form['username'].value if 'username' in form else ""
print(response.format("value="+username))
