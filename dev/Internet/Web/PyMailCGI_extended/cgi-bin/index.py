import cgi
import sys

from config import *


sys.stdout.reconfigure(encoding="utf-8")


response = """<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    {redirect}
    <title>PyMailCGI Main Page</title>
    <link rel="icon" href="../img/pylove.ico" type="image/x-icon">
</head>
<body>
    <form method="post">
        <table align="right">
        <tr><td><b>Personal area</b>
        <input type="hidden" name="s_id" value="{session_id}">
        <input type="hidden" name="username" value="{username}">
        <input type="submit" value="{username}" formaction="personal_area.py"></td>
        <td><input type="submit" value="Logout" formaction="logout.py">
        </td></tr></table>        
    </form>
    <br><br>
    <h1 align="center">PyMailCGI</h1>
    <h2 align="center">A IMAP/SMTP Web Email Interface</h2>
    <p align="center">
        <i>Version 1.0 March __ 2019</i>
    </p>
    <hr><h2>Действия</h2>
    <form method="post">
        <table>
        <tr><td><input type="hidden" name="s_id" value="{session_id}"></tr></td>
        <tr><td><input type="submit" value="Отправить сообщение по SMTP" formaction="send.py"></td></tr>
        <tr><td><input type="submit" value="Просмотреть сообщения на [imap_username]" formaction="fetch.py"></td></tr>
        </table>
    </form>
    <hr>
    <h2>Обзор</h2>
    <p>
        <a href="https://www.python.org/">
            <img src="../img/pylove.png"
                 height="100" width="100"
                 align="left"  hspace="10">
        </a>
        Этот сайт реализует простой веб-интерфейс к учетной записи электронной
        почты по протоколам IMAP/SMTP. С помощью этого интерфейса любой желающий
        сможет отправить письмо, но из-за ограничений безопасности вы не сможете
        просматривать электронную почту, не определив параметры своей учетной
        записи на почтовом сервере. Веб-приложение PyMailCgi реализовано как набор
        CGI-сценариев на языке Python, выполняющихся на сервере (не на вашем
        локальном компьютере) и генерирующих разметку HTML при взаимодействии
        с броузером. Подробности <i><a href="https://github.com/burkovski">
        смотрите на GitHub</a></i>.
    </p>
    <br><hr>
    <h2>Примечания</h2>
    <p>
        Эта версия
        не такая быстрая и полнофункциональная, как хотелось бы (например, каждый
        щелчок запускает выполнение операции через Интернет, здесь отсутствует
        операция сохранения электронной почты и не поддерживается многопоточный
        режим выполнения, кроме того, здесь не предусматривается кэширование
        заголовков или уже просмотренных сообщений). С другой стороны, PyMailCgi
        может взаимодействовать с любым веб-броузером и не требует устанавливать
        Python на ваш компьютер.
    </p>
    <p>
        Если вы решите использовать эти сценарии для чтения своей почты,
        то следует учесть, что PyMailCgi не гарантирует безопасность пароля вашей
        учетной записи. Смотрите примечания в странице операции просмотра сообщения.
    </p>
</body>
</html>
"""

form = cgi.FieldStorage()
session_id = form.getvalue(FormFields.session_id, None)
username = form.getvalue(FormFields.username, "Unknown")
redirect = ('<meta http-equiv="refresh" content="1;http://localhost/index.html">'
            if session_id is None else '')

print(response.format(redirect=redirect, session_id=session_id, username=username))
