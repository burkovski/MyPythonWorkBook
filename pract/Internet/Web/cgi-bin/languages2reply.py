"""
То же самое, но проще для сопровождения, использует строки шаблонов
разметки HTML, получает таблицу со списком языков и имя входного параметра
из общего модуля и импортирует многократно используемый модуль
имитации полей форм для нужд тестирования.
"""

import sys
import cgi
import html

from form_mockup import FieldMockup                    # имитация полей ввода
from languages2common import input_key, hellos         # общая таблица, имя параметра


sys.stdout.reconfigure(encoding="utf-8")
debug_me = False
html_head = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Languages 2</title>
</head>"""
html_body = """
<h3>{lang}</h3>
<p>
    <pre>{hello}</pre>    
</p><br>
"""


def show_hello(form):               # Разметка HTML для одного языка
    choice = form[input_key].value
    try:
        syntax = hellos[choice]
    except KeyError:
        syntax = "Sorry - I don't know this language!"
    return html_body.format(lang=html.escape(choice), hello=html.escape(syntax))


def main():
    if debug_me:
        form = {input_key: FieldMockup(sys.argv[1])}        # Имя в ком. строке
    else:
        form = cgi.FieldStorage()                           # Разбор действительный данных
    response = html_head
    if input_key not in form or form[input_key].value == "All":
        for lang in hellos:
            mockup = {input_key: FieldMockup(lang)}
            response += show_hello(mockup)
    else:
        response += show_hello(form)
    response += "<hr>"
    print(response)


if __name__ == "__main__":
    main()
