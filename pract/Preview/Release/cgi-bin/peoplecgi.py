import cgi
import html
import shelve
import sys
import os
shelve_name = "class-shelve"    # Файлы хранилища находятся в текущем каталоге

field_names = ('name', 'age', 'job', 'pay')

form = cgi.FieldStorage()           # Парсинг данных формы
print("Content-type: text/html")    # Заголовок + пустая строка для ответа
sys.path.insert(0, os.getcwd())     # Благодаря этой строке, модуль pickle и сам сценарий
                                    # будут способны импортировать модуль initdata

# Главный шаблон разметки html
reply_html = """
<html>
<title>People Input Form</title>
<body>
<form method=POST action="peoplecgi.py">
    <table>
    <tr><th>key<td><input type=text name=key value="%(key)s">
    $ROWS$
    </table>
    <p>
    <input type=submit value="Fetch" name=action>
    <input type=submit value="Update" name=action>
</form>
</body></html>
"""

# Вставить разметку html с данными в позицию $ROWS$
row_html = '<tr><th>%s<td><input type=text name=%s value="%%(%s)s">'
rows_html = ''
for fn in field_names:
    rows_html += (row_html % ((fn, ) * 3))
reply_html = reply_html.replace("$ROWS$", rows_html)


def html_size(adict):
    new = adict.copy()                          # Значения могут содержать &, >
    for field in field_names:                   # и другие специальные символы,
        value = new[field]                      # отображаемые особым образом
        new[field] = html.escape(repr(value))   # их необходимо экранировать
    return new

def fetchRecord(db, form):
    try:
        key = form['key'].value
        record = db[key]
        fields = record.__dict__        # Для заполнения строки ответа
        fields['key'] = key             # использовать словарь атрибутов
    except KeyError:
        fields = dict.fromkeys(field_names, '?')
        fields['key'] = "Missing or invalid key!"
    return fields

def updateRecord(db, form):
    if 'key' not in form:
        fields = dict.fromkeys(field_names, '?')
        fields['Key'] = "Missing key input!"
    else:
        key = form['key'].value
        if key in db:
            record = db[key]                # Изменить существующую запись
        else:
            from initdata import Person            # Создать/сохранить новую
            record = Person(name='?', age='?')     # для eval: строки в кавычках

        for field in field_names:
            setattr(record, field, eval(form[field].value))
        db[key] = record
        fields = record.__dict__
        fields['key'] = key
    return fields


db = shelve.open(shelve_name)
action = form['action'].value if 'action' in form else None
if action == 'Fetch':
    fields = fetchRecord(db, form)
elif action == 'Update':
    fields = updateRecord(db, form)
else:
    fields = dict.fromkeys(field_names, '?')            # Недопустимое значение
    fields['key'] = "Missing or invalid action!"        # кнопки формы отправки
db.close()
print(reply_html % html_size(fields))                   # заполнить форму ответа
