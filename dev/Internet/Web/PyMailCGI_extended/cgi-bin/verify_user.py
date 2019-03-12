import cgi
import shelve


response = """<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <title>Sign up</title>
    <link rel=icon href="../img/pylove.ico" type="image/x-icon">
</head>
<body>
    <h1>Verifying</h1>
    <hr>
    {0}
</body>
"""


form = cgi.FieldStorage()
username = form["username"].value
password = form["password"].value

with shelve.open(r"databases\users") as db:
    if username not in db:
        prompt = """<h3>Unknown user name: {}!</h3>"""
        link = """<br><a href="sign_up.py?username={}">Sign up</a>""".format(username)
    elif db[username]["password"] != password:
        prompt = """<h3>Invalid password for {}!</h3>"""
        link = """<br><a href="sign_in.py?username={}">Try again!</a>""".format(username)
    else:
        import os
        import datetime
        session_id = str(os.getpid()) + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        db[username]["session_id"] = session_id
        prompt = """<h3>Welcome, {}!</h3>"""
        link = """<form method="post" action="index.py">
            <input type="hidden" name="session_id" value="{0}">
            <input type="hidden" name="user" value="{1}">
            <input type="submit" value="Continue">
        </form>""".format(session_id, username)

print(response.format(
    prompt.format(username) + link
))


