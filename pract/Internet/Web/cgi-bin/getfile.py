#!/usr/bin/python
"""
Отображает содержимое любого сценария CGI (или другого файла), имеющегося
на стороне сервера, не выполняя его. Имя файла можно передать в параметре
строки URL или с помощью поля формы (используйте имя сервера "localhost",
если используется локальный сервер):
http://servername/cgi-bin/getfile.py?filename=somefile.html
http://servername/cgi-bin/getfile.py?filename=cgi-bin\somefile.py
http://servername/cgi-bin/getfile.py?filename=cgi-bin%2Fsomefile.py
Пользователи могут сохранить файл у себя, скопировав текст через буфер
обмена или воспользовавшись пунктом меню "View Source" ("Исходный код
страницы" или "Просмотр HTML-кода"). При обращении к этому сценарию из IE
для получения версии text/plain (formatted=False) может запускаться
программа Блокнот (Notepad), при этом не всегда используются символы конца
строки в стиле DOS; Netscape, напротив, корректно отображает текст на
странице броузера. Отправка файла в версии text/HTML действует в обоих типах
броузеров - текст правильно отображается на странице ответа в броузере.
Мы также проверяем имя файла, чтобы избежать отображения закрытых файлов;
в целом это может не предотвратить доступ к таким файлам: не устанавливайте
этот сценарий, если исходные тексты закрытых сценариев у вас не защищены
каким-то иным способом!
"""

import html
import cgi
import os
import sys


sys.stdout.reconfigure(encoding="utf-8")
formatted = True                               # True -> обернуть текст в HTML
privates = []# ["PyMail/cgi-bin/secret.py"]        # Эти файлы не показывать


try:
    same_file = os.path.samefile                # Проверка устройства, номера inode
except Exception:
    def same_file(path1, path2):
        abs_path1 = os.path.abspath(path1).lower()      # Близкая апроксимация
        abs_path2 = os.path.abspath(path2).lower()      # Нормализировать пути, привести к одному регистру
        return abs_path1 == abs_path2


template = """Content-type: {contype}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Getfile response</title>
</head>
<body>
    <h1>Source code for: {filename}</h1>
    <hr>
    <pre>{filetext}</pre>
    </hr>
</body>
</html>"""


def restricted(file_name):
    for path in privates:
        if same_file(file_name, path):
            return True     # Иначе вернет None ~ False


try:
    form = cgi.FieldStorage()
    filename = form["filename"].value      # Параметр URL или имя формы
except KeyError:
    filename = __file__                    # Иначе - имя файла по умолчанию

try:
    assert not restricted(filename)     # Загрузить, если не закрытый файл
    with open(filename, encoding=sys.getdefaultencoding()) as file:
        filetext = file.read()
except AssertionError:
    filetext = "(File access denied!)"
except Exception:
    filetext = "(Error opening file: {})".format(sys.exc_info()[1])


if formatted:
    response = template.format(
        contype="text/html",
        filename=filename,
        filetext=html.escape(filetext)
    )
else:
    response = "Content-type: text/plain\n\n{}".format(filetext)

print(response)
