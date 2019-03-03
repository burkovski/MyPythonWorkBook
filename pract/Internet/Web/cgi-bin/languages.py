#!/usr/bin/python
"""
демонстрирует синтаксис вывода сообщения 'hello world' на выбранном языке
программирования; обратите внимание, что в сценарии используются "сырые"
строки вида r'...', чтобы исключить интерпретацию последовательностей
символов '\n' в таблице, и к строкам применяется функция cgi.escape(), чтобы
такие строки, как '<<', корректно интерпретировались броузером - они будут
преобразованы в допустимый код разметки HTML; сценарию может быть передано
название любого языка программирования, так как в броузере можно явно ввести
полную строку URL вида "http://servername/cgi-bin/languages.py?language=
Cobol" или передать ее из сценария (с помощью urllib.request.urlopen).
предупреждение: список языков отображается в обеих версиях страницы,
CGI и HTML, - его можно было бы импортировать из общего файла,
если список выбора также генерируется сценарием CGI;
"""

import cgi
import html
import sys

sys.stdout.reconfigure(encoding="utf-8")

debug_me = False
input_key = "language"

hellos = {
    'Python': r" print('Hello World')               ",
    'Python2': r" print 'Hello World'                ",
    'Perl': r' print "Hello World\n";             ',
    'Tcl': r' puts "Hello World"                 ',
    'Scheme': r' (display "Hello World") (newline)  ',
    'SmallTalk': r" 'Hello World' print.               ",
    'Java': r' System.out.println("Hello World"); ',
    'C': r' printf("Hello World\n");           ',
    'C++': r' cout << "Hello World" << endl;     ',
    'Basic': r' 10 PRINT "Hello World"             ',
    'Fortran': r" print *, 'Hello World'             ",
    'Pascal': r" WriteLn('Hello World');            "
}


class Dummy:  # Имитация входного объекта
    def __init__(self, str):
        self.value = str


if debug_me:
    form = {input_key: Dummy(sys.argv[1])}  # Имя в командной строке
else:
    form = cgi.FieldStorage()

template = """Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Languages</title>
</head>
<body>
    <h1>Syntax</h1>
    <hr>
        {syntax}
    <hr>       
</body>
</html>
"""


def get_hello(form):
    hello_template = """<h3>{choice}</h3>
    <p><pre>{hello}</pre></p><br>\n
    """
    choice = form[input_key].value
    try:
        hello = html.escape(hellos[choice])
    except KeyError:
        hello = "Sorry - I don't know this language"
    return hello_template.format(choice=choice, hello=hello)


if input_key not in form or form[input_key].value == "All":
    syntax = ""
    for lang in hellos:
        mock = {input_key: Dummy(lang)}
        syntax += get_hello(mock)
else:
    syntax = get_hello(form)

print(template.format(syntax=syntax))
