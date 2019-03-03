"""
###########################################################################
использует модуль Python почтового интерфейса SMTP для отправки сообщений;
это простой сценарий одноразовой отправки - смотрите pymail, PyMailGUI
и PyMailCGI, реализующие клиентов с более широкими возможностями
взаимодействия с пользователями; смотрите также popmail.py - сценарий
получения почты, и пакет pop_mailtools, позволяющий добавлять вложения
и форматировать сообщения с помощью стандартного пакета email;
###########################################################################
"""

import smtplib
import sys
import email.utils
from mailtools import mailconfig

mail_server = mailconfig.smtp_servername
mail_user = mailconfig.pop_username
mail_password = "mr.Hedgehognumber1"  # getpass.getpass("Password for {}?".format(mail_server))

FROM = input("From? ").strip()          # или целевой сервер будет введен пользователем
TO = input("To? ").strip()
TO_SPLIT = TO.split(';')                # допускается список получателей
SUBJ = input("Subject? ").strip()
DATE = email.utils.formatdate()         # текущие время и дата, rfc2822

# стандартные заголвки, за которыми следует пустая строка и текст
text = "From: {} \nTo: {}\nDate: {}\nSubject: {}\n\n".format(FROM, TO, DATE, SUBJ)
print("Type message text, end with line=[Ctrl+D (Unix), Ctrl+Z (Windows)]")
while True:
    line = sys.stdin.readline()
    if not line:
        break           # выход по ctrl+z/d
    if line[:4] == "From":
        line = '>' + line
    text += line

print("Connecting...")
server = smtplib.SMTP_SSL(mail_server)
server.login(mail_user, mail_password)
failed = server.sendmail(FROM, TO_SPLIT, text)
server.quit()
if failed:
    print("Failed recipients: {}".format(failed))
else:
    print("OK! No errors.")
print("Bye.")
