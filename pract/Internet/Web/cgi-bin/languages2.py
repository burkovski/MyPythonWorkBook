#!/usr/bin/python
"""
разметка HTML главной страницы генерируется сценарием Python, а не готовым
файлом HTML; это позволяет импортировать ожидаемое имя поля ввода и значения
таблицы выбора языков из общего файла модуля Python; теперь изменения нужно
выполнять только в одном месте, в файле модуля Python;
"""


from languages2common import hellos, input_key
import sys
sys.stdout.reconfigure(encoding="utf-8")


REPLY = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Languages 2</title>
</head>
<body>
    <h1>Hello World selector</h1>
    <p>
        Эта страница похожа на страницу в файле <a href="../languages.html">
        languages.html</a>, но генерируется динамически с помощью сценария CGI
        на языке Python, используемый здесь список выбора и имена полей ввода
        импортируются из общего модуля Python на сервере. При добавлении новых
        языков достаточно будет изменить только общий модуль, потому что он
        совместно используется сценариями, производящими страницы ответа.
        
        Чтобы увидеть программный код, генерирующий эту страницу и ответ, щелкните
        <a href="getfile.py?filename=cgi-bin\languages2.py">здесь</a>,
        <a href="getfile.py?filename=cgi-bin\languages2reply.py">здесь</a>,
        <a href="getfile.py?filename=cgi-bin\languages2common.py">здесь</a> и
        <a href="getfile.py?filename=cgi-bin\\form_mockup.py">здесь</a>.</P>
        <hr>
    </p>
    <form method="post" action="languages2reply.py">
        <p><b>Select a programming language:</b></p>
        <p>
        <select name={name}>
            <option>All</option>
            {hellos}
            <option>Other</option>
        </select>
        </p>
        <p><input type="submit"></p>
    </form>
    <hr>
</body>
</html>
"""


print(REPLY.format(
    name=input_key,
    hellos='\n\t\t\t'.join("<option>{}</option>".format(lang) for lang in hellos)
))
