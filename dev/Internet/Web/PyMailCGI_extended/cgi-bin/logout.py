import html_layout
import cgi
import database.dbmanager as db_manager
import os

from http.cookies import SimpleCookie
from config import *


form = cgi.FieldStorage()
options = {key: form.getvalue(key) for key in form}
username = options.get(FormFields.username)
key = options.get(FormFields.session_id)


if username and key:
    with db_manager.DataBaseManager(DBResponse.path) as dbm:
        dbm.update(
            DBResponse.users_table,
            DBUsersFields.session,
            "NULL",
            DBUsersFields.username,
            username
        )
    cook_str = os.environ.get("HTTP_COOKIE")
    cookies = SimpleCookie(cook_str)
    user_cook = cookies.get(FormFields.session_id)  # Извелчь, если был отправлен
    if user_cook is not None:  # Создать при первом посещении
        cookies[FormFields.session_id] = "invalid"
        cookies[FormFields.session_id]["Expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
        print(cookies)
    response = html_layout.HTMLMaker(options)
    response.page_header()
    print("<h3>Logout successful</h3>")
    response.page_footer()
