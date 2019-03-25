import cgi
import html
import urllib.parse
import sys
import os
import mailtools

from mailtools import mailconfig


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr = sys.stdout
parser = mailtools.MailParser()
url_root = ''


def page_header(app="PyMailCGI", color="#FFFFFF", kind="main", info=""):
    print("""<!DOCTYPE html>\n
    <head>
        <title>{app}: {kind} page</title>
        <meta charset="UTF-8">
        <link rel="icon" href="../img/pylove.ico" type="image/x-icon">
    </head>
    <body bgcolor="{color}">
    <header>
        <h1>{app} {info}</h1><hr></header>""".format(app=app, kind=kind, color=color,
                                                     info=(info or kind)))


def page_footer(root="index.html"):
    print("""<footer><hr><table><tr>
    <td><a href="https://www.python.org" target="_blank">
    <img src="../img/pylove_thumb.png"></a><td>
    <td><a href="https://github.com/burkovski" target="_blank">
    <img src="../img/github_logo_text.png" hspace="5"></a></td>
    <th><a href="../{root}">Back to root page</a></th>
    </tr></table></footer>
    </body></html>""".format(root=root))


def password_page(mode):
    modes = {
        "SMTP": {"script": "on_view_smtp_password_submit.py",
                 "getter": get_standard_smtp_fields},
        "IMAP": {"script": "on_view_imap_password_submit.py",
                 "getter": get_standard_imap_fields}
    }
    if mode not in modes:
        raise KeyError("Invalid mode: <{}>".format(mode))
    user, _, host = modes[mode]["getter"]({})
    page_header(kind="{} password input".format(mode))
    print("""<form method="post" action="{0}{1}">
    <p>Введите пароль учетной записи пользователя "{2}" на сервере IMAP "{3}".</p>
    <p>
        <input type="password" name="password">
        <input type="submit" value="Отправить">
    </p>
    </form><hr>
    <p><i>Примечание, касающееся безопасности</i>: Пароль, введенный
    в поле выше, будет отправлен на сервер через Интернет, но он нигде
    не отображается, никогда не передается в паре с именем пользователя
    в незашифрованном виде и нигде не сохраняется: ни на сервере (он только
    передается последующим страницам в скрытых полях форм), ни на стороне
    клиента (система не генерирует никаких cookies). Тем не менее, полная
    безопасность не гарантируется; при работе с PyMailCGI вы можете
    использовать кнопку "Назад" ("Back") своего броузера в любой
    момент времени.</p>
    """.format(url_root, modes[mode]["script"], user, host))
    page_footer()


def format_link(cgi_url, params):
    params = urllib.parse.urlencode(params)
    return "{}?{}".format(cgi_url, params)


def create_form(cgi_url, params):
    form = """<form method="post" action="{}" style="display: inline-block; margin: 0;">""".format(cgi_url)
    for (key, value) in params.items():
        form += """<input type="hidden" name="{}" value="{}">""".format(key, value)
    form += """<input type="submit" value="View"></form>"""
    return form


def page_list_simple(links_list):
    print("<ol>")
    for (text, cgi_url, params) in links_list:
        link = format_link(cgi_url, params)
        text = html.escape(text)
        print('<li><a href="{}">\n {}</li>'.format(link, text))
    print("</ol>")


def page_list_table(links_list):
    print("""<p><table border>""")
    for (text, cgi_url, params) in links_list:
        form = create_form(cgi_url, params)
        text = ' '.join(text.split(' ')[:-2])
        text = html.escape(text)
        print("""<tr><td><pre>{}</pre></td>
        <td style="vertical-align: middle;">{}</td></tr>""".format(text, form))
    print("</table></p>")


def list_page(links_list, kind="selection list"):
    page_header(kind=kind)
    page_list_table(links_list)
    page_footer()


def message_area(headers, text, extra=''):
    address_headers = {"From", "To", "Cc", "Bcc"}
    print("<table cellpadding=3>")
    for hdr in ("From", "To", "Cc", "Subject"):
        raw_hdr = headers.get(hdr, '?')
        parser_type = (parser.decode_address_header
                       if hdr in address_headers else parser.decode_header)
        decoded = parser_type(raw_hdr)
        escaped = html.escape(decoded, quote=True)
        print("""<tr><th align="right">{hdr}:</th>
        <td><input type="text" name="{hdr}" 
                   value="{value}" {extra} size="60"></td>
        </tr>""".format(hdr=hdr, value=escaped, extra=extra))
    print("""<tr><th align="right">Text:</th>
    <td><textarea name="Text" cols="80" rows="10" {extra}>{text}\n</textarea>
    </td></tr></table>""".format(extra=extra, text=html.escape(text) if text else '?'))


def view_attachment_links(part_names):
    print('<hr><table border cellpadding="3"><tr><th>Parts:</th>')
    for filename in part_names:
        basename = os.path.basename(filename)
        filename = os.path.normpath(filename)
        print("""<td><a href="../{path}" target="_blank">{name}</a></td>""".format(path=filename, name=basename))
    print("</tr></table><hr>")


def view_page(msg_num, headers, text, form, parts=None):
    page_header(kind="View")
    user, password, host = list(map(html.escape, get_standard_imap_fields(form)))
    print("""<form method="post" action="{root}on_view_page_action.py">
    <input type="hidden" name="msg_num" value="{msg_num}">
    <input type="hidden" name="user" value="{user}">
    <input type="hidden" name="host" value="{host}">
    <input type="hidden" name="password" value="{password}">""".format(
        root=url_root,
        msg_num=msg_num,
        user=user,
        host=host,
        password=password
    ))
    message_area(headers, text, "readonly")
    if parts: view_attachment_links(parts)
    print("""<input type="hidden" name="Date" value="{date}">
    <table><tr><th align="right">Action:</th>
    <td><select name="action">
    <option>Reply</option>
    <option>Forward</option>
    <option>Delete</option></select></td>
    <td><input type="submit" value="Next"></td></tr>
    </table></form>""".format(date=headers["Date"]))
    page_footer()


def send_attachments_widgets(max_attach=3):
    print("<p><b>Attach:</b><br>")
    for i in range(1, max_attach+1):
        print('<input type="file" size=80 name="attach{}"><br>'.format(i))
    print("</p>")


def edit_page(kind, password, headers=None, text=''):
    if not headers:
        headers = {}
    page_header(kind=kind)
    print("""<p><form enctype="multipart/form-data" method="post" action="{}on_edit_page_send.py">
    <input type="hidden" name="password" value="{}">""".format(url_root, password))
    if mailconfig.my_signature:
        text = "{}\n{}\n".format(text, mailconfig.my_signature)
    message_area(headers, text)
    send_attachments_widgets()
    # print("<h1>Password: {}</h1>".format(password))
    print("""<input type="submit" value="Send">
    <input type="reset" value="Reset"></form></p>""")
    page_footer()


def error_page(message, stack_trace=True, form=None):
    page_header(kind="Error")
    if form:
        print("<ol>")
        for key in form:
            value = form.getvalue(key)
            if key.startswith("attach") and value: value = form[key].filename
            print('<li>key=[{}] value=[{}]</li>'.format(key, value))
        print("</ol>")
    exc_type, exc_value, exc_tb = sys.exc_info()
    print("""<h2>Error Description</h2><p>{msg}</p>
    <h2>Python Exception</h2><p>{type}</p>
    <h2>Exception details</h2><p>{val}</p>""".format(
        msg=message,
        type=html.escape(str(exc_type)),
        val=html.escape(str(exc_value))
    ))
    if stack_trace:
        from traceback import print_tb
        print("""<h2>Exception traceback</h2>
        <p><pre>{}</pre></p>""".format(print_tb(exc_tb, None, sys.stdout)))
    page_footer()


def confirm_page(kind, form=None):
    page_header(kind="Confirmation")
    if form:
        print("<ol>")
        for key in form:
            value = form.getvalue(key)
            if key.startswith("attach") and value: value = form[key].filename
            print('<li>key=[{}] value=[{}]</li>'.format(key, value))
        print("</ol>")
    print("""<h2>{} operation was successful</h2>
    <p>Press the link below to return to the main page.</p>""".format(kind))
    page_footer()


def get_field(form, field, default=''):
    return form[field].value if field in form else default


def get_standard_imap_fields(form):
    return (
        get_field(form, "user", mailconfig.imap_username),
        get_field(form, "password", '?'),
        get_field(form, "host", mailconfig.imap_servername)
    )


def get_standard_smtp_fields(form):
    return (
        get_field(form, "user", mailconfig.smtp_username),
        get_field(form, "password", '?'),
        get_field(form, "host", mailconfig.smtp_servername)
    )


def run_silent(func, *args):
    class Silent:
        def write(self, *pargs, **kwargs):
            pass
    sys.stdout = Silent()
    try:
        result = func(*args)
    finally:
        sys.stdout = sys.__stdout__
    return result


def dump_state_page(exhaustive=False):
    if exhaustive:
        cgi.test()
    else:
        page_header(kind="state dump")
        form = cgi.FieldStorage()
        cgi.print_form(form)
        page_footer()
    sys.exit()
