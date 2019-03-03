#!/usr/bin/python
"""
извлекает файл, выгруженный веб-броузером по протоколу HTTP; пользователи
открывают страницу putfile.html, чтобы получить страницу с формой выгрузки,
которая затем запускает этот сценарий на сервере; способ очень мощный
и очень опасный: обычно желательно проверять имя файла и так далее; выгрузка
возможна, только если файл или каталог доступен для записи: команды Unix
'chmod 777 uploads' может оказаться достаточно; путь к файлу поступает
в формате пути на стороне клиента: его требуется обработать здесь;
предупреждение: выходной файл можно было бы открыть в текстовом режиме,
чтобы подставить символы конца строки, используемые на принимающей
платформе, поскольку содержимое файла всегда возвращается модулем cgi
в виде строки str, но это временное решение - модуль cgi в 3.1 вообще
не поддерживает выгрузку двоичных файлов;
"""

import os
import sys
import cgi
import html
import posixpath        # Для обработки клиентских путей
import ntpath


debug_mode = False              # True=вывод данных формы
load_text_auto = False          # True=читать файл целиком
upload_dir = os.path.join('.', 'uploads')        # Каталог для сохранения файлов

sys.stderr = sys.stdout         # Для вывода ошибок
form = cgi.FieldStorage()       # Выполнить анализ данных формы


html_reply = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Getfile: response page</title>
</head>
<body>
    <h1>Putfile response page</h1><hr>
    {body}
</body>
</html>
"""

reply_ok = html_reply.format(body="""
<p>Your file, {filename}, hs been saved on the server as {srvr_filename}.</p>
<p>An echo of the file's content  received and saved appears bellow.</p><hr>
<p><pre>
{filecontent}
</pre></p>
<hr>
""")


# Обработка даных формы
def split_path(orig_path):           # Получить имя файла без пути
    for path_module in posixpath, ntpath:      # Проверить все типы
        base_name = path_module.split(orig_path)[1]
        if base_name != orig_path:
            return base_name             # Пробелы допустимы
    return orig_path                     # Неудача или имя файла не содержит путь к каталогу


def save_on_server(file_info):           # Поле с именем data
    base_name = split_path(file_info.filename)     # Имя файла без пути
    srvr_filename = os.path.join(upload_dir, base_name)      # В каталого, если он указан
    with open(srvr_filename, 'wb') as srvr_file:       # Всегда в двоичном режиме
        if load_text_auto:
            filetext = file_info.value               # Прочитать текст в строку
            srvr_file.write(filetext)               # Сохранить на сервере
        else:                                   # Иначе - читать построчно
            num_lines, filetext = 0, b''
            for line in file_info.file:
                srvr_file.write(line)
                filetext += line
                num_lines += 1
            filetext = "[Lines={}]\n\n".format(num_lines).encode() + filetext
    try:
        filetext = filetext.decode()
    except UnicodeDecodeError:
        filetext = "No text file!"
    os.chmod(srvr_filename, 0o666)          # Разрешить запись: владелец Nobody
    return filetext, srvr_filename


def main():
    if "clientfile" not in form:
        response = html_reply.format(body="Error: no file was received!")
    elif not form["clientfile"].filename:
        response = html_reply.format(body="Error: file name is missing!")
    else:
        file_info = form['clientfile']
        try:
            filetext, srvr_filename = save_on_server(file_info)
        except Exception:
            err_msg = "<h2>Error</h2><p>{0}</p><p>{1}</p>".format(*tuple(sys.exc_info()[:2]))
            response = html_reply.format(body=err_msg)
        else:
            kwargs = {
                "filename": html.escape(file_info.filename),
                "srvr_filename": html.escape(srvr_filename),
                "filecontent": html.escape(filetext)
            }
            response = reply_ok.format(**kwargs)
    print(response)


main()
