import cgi


response = """<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <title>Sign up</title>
    <link rel=icon href="../img/pylove.ico" type="image/x-icon">
</head>
<body>
    <h1>Register</h1>
    <hr>
    {0}
</body>
"""

form = cgi.FieldStorage()
try:
    username = form["username"].value
    password = form["password"].value
    rep_pass = form["rep_password"].value
except KeyError:
    body = """<h3>You must type all fields</h3><br><a href="sign_up.py">Try again!</a>"""
    print(body)
else:
    if password != rep_pass:
        body = """<h3>Password don't match</h3><br><a href="sign_up.py?username={}">Try again!</a>"""
    else:
        import shelve
        with shelve.open(r"databases\users") as db:
            if username in db:
                body = """<h3>User already exist!</h3><br><a href="sign_in.py?username={}">Sign in!</a>"""
            else:
                db[username] = {
                    "user":       username,
                    "password":   password,
                    "session_id": None,
                }
                body = "<h3>Registered {} successfully</h3>"
    print(response.format(body.format(username)))
values = {key: form[key].value for key in form}
print(values)
