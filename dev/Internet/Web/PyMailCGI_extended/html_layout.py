import html
import urllib.parse
import sys
import os
import mailtools

from config import*
from mailtools import mailconfig


sys.stdout.reconfigure(encoding="utf-8")
# sys.stderr = sys.stdout

parser = mailtools.MailParser()

url_root = ''


class HTMLMaker:
    def __init__(self, options, app="PyMailCGI", color="#FFFFFF"):
        self.options = options
        # self.form = form or cgi.FieldStorage()
        self.app = app
        self.color = color
        self.root = "../index.html"

    def page_header(self, info=None):
        print("""<!DOCTYPE html>\n
        <head>
            <title>{app}: {kind}</title>
            <meta charset="UTF-8">
            <link rel="icon" href="../img/pylove.ico" type="image/x-icon">
        </head>
        <body bgcolor="{color}">
            <header>
                <h1>{app} {info}</h1><hr>
            </header>""".format(
                app=self.app,
                color=self.color,
                kind=self.options.get("kind", "page"),
                info=(info or self.options.get("kind"))
            )
        )

    def page_footer(self):
        print("""</body><footer><hr><table><tr>
        <td><a href="https://www.python.org" target="_blank">
        <img src="../img/pylove_thumb.png"></a><td>
        <td><a href="https://github.com/burkovski" target="_blank">
        <img src="../img/github_logo_text.png" hspace="5"></a></td>
        <th><a href="../{root}">Back to root page</a></th>
        </tr></table></footer>
        </body></html>""".format(root=("cgi-bin/index.py?username={}".format(
            self.options.get("username"))
            if self.options.get("session_id")
            else self.root))
        )

    def print_options_fields(self):
        self.page_header()
        for key in self.options:
            print("<h3>{} => {}</h3>".format(key, self.options.get(key, '?')))
        self.page_footer()

    def render_table(self, row_pattern, rows):
        print("<table>")
        for row in rows:
            print(row_pattern.format(**row))
        print("</table>")

    def password_page(self):
        username = self.options.get(FormFields.username, '')
        extra_fields = self.options.get(OptionsKeys.extra_fields, '')
        verify_mode = self.options.get(FormFields.verify_mode)
        row_pattern = """<tr>
        <th align="left">{caption}<th>
        <td>{field}</td>
        </tr>"""
        rows = [{"caption": "User name:",
                 "field": '<input type="text" name="{0}" value="{1}">'.format(FormFields.username, username)},
                {"caption": "Password:",
                 "field": '<input type="password" name="{0}">'.format(FormFields.password)},
                {"caption": '',
                 "field": '<input type="submit" value="Send">'},
                {"caption": '',
                 "field": '<input type="hidden" name="{0}" value="{1}">'.format(FormFields.verify_mode, verify_mode)}]
        if extra_fields: rows.insert(-2, extra_fields)
        self.page_header()
        print('<form method="post" action="{}">'.format(self.options.get(FormFields.handler_script)))
        self.render_table(row_pattern, rows)
        print("</form>")
        self.page_footer()

    def prompt_page(self):
        self.page_header()
        print("""<h3>{0}</h3><form method="post" action="{1}"><table>""".format(
            self.options[OptionsKeys.prompt],
            self.options[FormFields.handler_script]
        ))
        key = self.options.get(FormFields.session_id, None)
        if key:
            print('<tr><input type="hidden" name="{}" value="{}"></tr>'.format(FormFields.session_id, key))
        print("""<tr><input type="hidden" name="username" value="{0}"></tr>
        <tr><input type="submit" value="{1}"></tr></table>
        </form>""".format(self.options[FormFields.username], self.options[FormFields.submit_button_caption]))
        self.page_footer()







