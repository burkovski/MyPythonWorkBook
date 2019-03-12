"""
############################################################################
использует модуль POP3 почтового интерфейса Python для просмотра сообщений
почтовой учетной записи pop; это простой листинг - смотрите реализацию
клиента с большим количеством функций взаимодействий с пользователем
в pymail.py и сценарий отправки почты в smtpmail.py; протокол POP
используется для получения почты и на сервере выполняется на сокете
с портом номер 110, но модуль Python poplib скрывает все детали протокола;
для отправки почты используйте модуль smtplib (или os.popen('mail...')).
Смотрите также модуль imaplib, реализующий альтернативный протокол IMAP,
и программы PyMailGUI/PyMailCGI, реализующие дополнительные особенности;
############################################################################
"""

import poplib
import getpass
from mailtools import mailconfig

mail_server = mailconfig.pop_servername
mail_user = mailconfig.pop_username
mail_password = getpass.getpass("Password for {}?".format(mail_server))


print("Connecting...")
server = poplib.POP3_SSL(mail_server)
server.user(mail_user)                      # соединение и регистрация на сервере
server.pass_(mail_password)

try:
    print(server.getwelcome())
    msg_count, msg_bytes = server.stat()
    print("There are {} mail messages in {} bytes".format(msg_count, msg_bytes))
    print(server.list())
    print("-" * 80)
    input("[Press Enter key]")
    for i in range(msg_count):
        header, message, octects = server.retr(i+1)      # octects - счетчик байтов
        for line in message:                             # читает, выводит все письма
            print(line.decode())                         # сообщения в bytes
        print("-" * 80)                                  # почтовый ящик блокирется до выозва quit
        if i < msg_count - 1:
            input("[Press Enter key]")
finally:
    server.quit()                   # снять блокировку с ящика, иначе - будет разблокирован по таймауту
print("Bye.")
