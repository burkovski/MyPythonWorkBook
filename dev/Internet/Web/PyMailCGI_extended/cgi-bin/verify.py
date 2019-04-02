import html_layout
import cgi
import database.dbmanager
import os
import datetime

from http.cookies import SimpleCookie
from config import *


class UserInteraction:
    db_table = DBResponse.users_table
    db_username = DBUsersFields.username
    db_password = DBUsersFields.password
    db_session = DBUsersFields.session

    def __init__(self, form):
        self.form = form
        self.mode = form.getvalue(FormFields.verify_mode)
        self.username = form.getvalue(FormFields.username)
        self.password = form.getvalue(FormFields.password)
        self.repeat_password = None
        self.options = {FormFields.username: self.username, FormFields.session_id: None}

    def interact(self):
        with database.dbmanager.DataBaseManager(DBResponse.path) as db_manager:
            if self.mode == FormFields.vm_sign_in:
                self.login_user(db_manager)
            elif self.mode == FormFields.vm_sign_up:
                self.repeat_password = form.getvalue(FormFields.repeat_password)
                self.create_user(db_manager)

    def login_user(self, dbm):
        if not dbm.contains(self.db_table, self.db_username, self.username):
            params = [(OptionsKeys.kind, "Wrong name"),
                      (OptionsKeys.prompt, "Unknown user name: {0}. Try to sign up with this name!"),
                      (FormFields.handler_script, "sign_up.py"),
                      (FormFields.submit_button_caption, "Sign up!")]
        elif self.password != dbm.fetch_one(self.db_table, self.db_password, self.db_username, self.username)[0]:
            params = [(OptionsKeys.kind, "Wrong password"),
                      (OptionsKeys.prompt, "Wrong password for: {0}. Try to sign in again!"),
                      (FormFields.handler_script, "sign_in.py"),
                      (FormFields.submit_button_caption, "Sign in!")]
        else:
            key = dbm.fetch_one(self.db_table, self.db_session, self.db_username, self.username)[0]
            if not key:
                key = "{}_{}".format(str(os.getpid()), datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
                dbm.update(self.db_table, self.db_session, key, self.db_username, self.username)
            cook_str = os.environ.get("HTTP_COOKIE")
            cookies = SimpleCookie(cook_str)
            user_cook = cookies.get(FormFields.session_id)  # Извелчь, если был отправлен
            if user_cook is None:  # Создать при первом посещении
                cookies = SimpleCookie()  # Вывести заголовок Set-cookie
                cookies[FormFields.session_id] = key
                print(cookies)
            params = [(OptionsKeys.kind, "Welcome"),
                      (OptionsKeys.prompt, "Welcome, {0}!"),
                      (FormFields.handler_script, "index.py"),
                      (FormFields.session_id, key),
                      (FormFields.submit_button_caption, "Continue"),
                      (FormFields.session_id, key)]
            params[1] = (params[1][0], params[1][1].format(self.username))
        self.options.update(params)

    def create_user(self, dbm):
        if self.password != self.repeat_password:
            params = [(OptionsKeys.kind, "Mismatch passwords"),
                      (OptionsKeys.prompt, "Password must be match. Try again as {}!".format(self.username)),
                      (FormFields.handler_script, "sign_up.py"),
                      (FormFields.submit_button_caption, "Sign up!")]
        else:
            if dbm.contains(self.db_table, self.db_username, self.username):
                params = [(OptionsKeys.kind, "Wrong username"),
                          (OptionsKeys.prompt, "This user already exist. Sign in as {}!"),
                          (FormFields.handler_script, "sign_up.py"),
                          (FormFields.submit_button_caption, "Sign up!")]
            else:
                params = [(OptionsKeys.kind, "Sign up successful"),
                          (OptionsKeys.prompt, "Your account was created. Continue as {}."),
                          (FormFields.handler_script, "sign_in.py"),
                          (FormFields.submit_button_caption, "Sign in!")]
                dbm.dump(self.db_table, (self.db_username, self.db_password), (self.username, self.password))
        self.options.update(params)


form = cgi.FieldStorage()
i = UserInteraction(form)
i.interact()
response = html_layout.HTMLMaker(i.options)
response.prompt_page()
