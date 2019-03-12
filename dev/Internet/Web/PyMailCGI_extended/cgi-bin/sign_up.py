import cgi


form = cgi.FieldStorage()

response = """<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <title>Sign up</title>
    <link rel=icon href="../img/pylove.ico" type="image/x-icon">
</head>
<body>
    <h1>Sign Up!</h1>
    <hr>
    <form method="post" action="register_user.py"><table>
    <tr>
        <th align="left">User name:</th>
        <td><input type="text" name="username" value={}></td>
    </tr>
    <tr>
        <th align="left">Password:</th>
        <td><input type="password" name="password"></td>
    </tr>
    <tr>
        <th align="left">Repeat password:</th>
        <td><input type="password" name="rep_password"></td>
    </tr>
    <tr>
        <th></th>
        <td colspan="2"><input type="submit" value="Send"></td>
    </tr>
    </table></form>
</body>
"""

username = form['username'].value if 'username' in form else ""
print(response.format(username))
