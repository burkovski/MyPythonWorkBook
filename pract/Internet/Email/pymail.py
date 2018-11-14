"""
##########################################################################
pymail - простой консольный клиент электронной почты на языке Python;
использует модуль Python poplib для получения электронных писем,
smtplib для отправки новых писем и пакет email для извлечения
заголовков с содержимым и составления новых сообщений;
##########################################################################
"""

import poplib
import smtplib
import email.utils
import mailconfig


from email.parser import Parser
from email.message import Message
from email.header import decode_header


fetch_encoding = mailconfig.fetch_encoding


def decode_to_unicode(message_bytes, fetch_encoding=fetch_encoding):
    """
    декодирует извлекаемые строки bytes в строки str Юникода
    для отображения или анализа; использует глобальные настройки
    (или значения по умолчанию для платформы, исследует заголовки, делает
    обоснованные предположения); в Python 3.2/3.3 этот шаг может оказаться
    необязательным: в этом случае достаточно будет просто вернуть
    сообщение нетронутым;
    """
    return [line.decode(fetch_encoding) for line in message_bytes]


def split_addrs(field):
    """
    разбивает список адресов по запятым, учитывает возможность
    появления запятых в именах
    """
    pairs = email.utils.getaddresses([field])                   # [(name, addr)]
    return [email.utils.formataddr(pair) for pair in pairs]     # [name <addr>]


def input_message():
    import sys
    From = input("From? ").strip()
    To = input("To? ").strip()                          # заголовок Date устанавливается автоматически
    To = split_addrs(To)                                # допускается множество, name+<addr>
    Subj = input("Subj? ").strip()                   # не разбивать вслепую по ',' или ';'
    print("Type message text, end with line=[Ctrl+D (Unix), Ctrl+Z (Windows)]")
    text = ''
    while True:
        line = sys.stdin.readline()
        if not line: break
        text += line
    return From, To, Subj, text


def send_message(mail_user, mail_passwd):
    From, To, Subj, text = input_message()
    msg = Message()
    msg["From"] = From
    msg["To"] = ', '.join(To)                   # для заголовка, не для отправки
    msg["Subject"] = Subj
    msg["Date"] = email.utils.formatdate()      # текущая дата и время
    msg.set_payload(text)
    server = smtplib.SMTP_SSL(mailconfig.smtp_servername)
    try:
        server.login(mail_user, mail_passwd)
        failed = server.sendmail(From, To, msg.as_string())
    except Exception as exc:
        print("Error - send failed!", exc)
    else:
        if failed: print("Failed: {}".format(failed))


def connect(server_name, user, passwd):
    print("Connecting...")
    server = poplib.POP3_SSL(server_name)
    server.user(user)           # соединиться, зарегистрироваться на сервере
    server.pass_(passwd)
    print(server.getwelcome())
    return server


def load_messages(server_name, user, passwd, load_from=1):
    server = connect(server_name, user, passwd)
    try:
        print(server.list())
        msg_count, msg_bytes = server.stat()
        print("There are {} mail messages in {} bytes".format(msg_count, msg_bytes))
        print("Retrieving...")
        msg_list = []
        for i in range(load_from, msg_count+1):
            hdr, message, octets = server.retr(i)           # сохранить текст в списке
            message = decode_to_unicode(message)
            msg_list.append('\n'.join(message))
    finally:
        server.quit()
    assert len(msg_list) == (msg_count - load_from) + 1
    return msg_list


def delete_messages(server_name, user, passwd, to_delete, verify=True):
    print("To be deleted: {}".format(to_delete))
    if verify and input("Delete?").strip()[:1] not in {'y', 'Y'}:
        print("Delete canceled.")
    else:
        server = connect(server_name, user, passwd)
        try:
            print("Deleting messages from server...")
            for msg_num in to_delete:           # повторно соединиться для удаления писем
                server.dele(msg_num)            # ящик будет заблокирован до вызова quit()
        finally:
            server.quit()


def show_index(msg_list):
    for (count, msg_text) in enumerate(msg_list, start=1):
        msg_hdrs = Parser().parsestr(msg_text, headersonly=True)
        for hdr_name in ("From", "To", "Date", "Subject"):
            try:
                hdr = msg_hdrs[hdr_name]
                binary, charset = decode_header(hdr)[0]
                if charset:
                    hdr = binary.decode(charset)
                print("\t{0:<8}=> {1}".format(hdr_name, hdr))
            except KeyError:
                print("\t{0:<8}=> (unknown)".format(hdr_name))
        print()
        if count % 5 == 0:
            input("[Press <Enter> key]")        # приостановка каждые 5 сообшений


def show_message(i, msg_list):
    if 1 <= i <= len(msg_list):
        print('-' * 79)
        msg = Parser().parsestr(msg_list[i-1])
        if msg.is_multipart():
            print("Multipart message, show text only, sorry!")
            msg = msg.get_payload(i=0)
        content = msg.get_payload(decode=True)    # содержимое: строка или [Messages]
        charset = msg.get_content_charset()
        if charset:
            content = content.decode(charset)
        if isinstance(content, str):
            content = content.rstrip() + '\n'  # сохранить только последний символ конца строки
        print(content)
        print('-' * 79)                          # получить только текст, см. email.parsers
    else:
        print("Bad message number!")


def save_message(i, mail_file, msg_list):
    if 1 <= i <= len(msg_list):
        save_file = open(mail_file, 'a', encoding=fetch_encoding)
        save_file.write('\n' + msg_list[i-1] + '-'*80 + '\n')
    else:
        print("Bad message number!")


def msg_num(command):
    try:
        return int(command.split()[1])
    except Exception:
        return -1


help_text = """
Available commands:
i    - index display
l ?n - list all messages (or just message n)
d ?n - mark all messages for deletion (or just message n)
s ?n - save all messages to a file (or just message n)
m    - compose and send a new mail message
q    - quit pytmail 
?    - display this help text  
"""


def interact(msg_list, mail_file, mail_user, mail_passwd):
    show_index(msg_list)
    to_delete = []
    while True:
        try:
            command = input("[Pymail] Action? {i, l, d, s, m, q, ?} ")
        except EOFError:
            command = 'q'
        if not command:
            command = '*'

        if command == 'q':
            break                       # завершение
        elif command[0] == 'i':         # оглавление
            print("Hello!")
            show_index(msg_list)
        elif command[0] == 'l':
            if len(command) == 1:
                for i in range(1, len(msg_list)+1):
                    show_message(i, msg_list)
            else:
                show_message(msg_num(command), msg_list)
        elif command[0] == 's':         # сохранение
            if len(command) == 1:
                for i in range(1, len(msg_list) + 1):
                    save_message(i, mail_file, msg_list)
            else:
                save_message(msg_num(command), mail_file, msg_list)
        elif command[0] == 'd':         # удаление
            if len(command) == 1:
                to_delete = list(range(1, len(msg_list)+1))
            else:
                del_num = msg_num(command)
                if (1 <= del_num <= len(msg_list)) and (del_num not in to_delete):
                    to_delete.append(del_num)
                else:
                    print("Bad message number!")
        elif command[0] == 'm':         # составление нового письма
            send_message(mail_user, mail_passwd)
        elif command[0] == '?':
            print(help_text)
        else:
            print("What? -- type '?' for a commands help")
    return to_delete


if __name__ == "__main__":
    import getpass
    try:
        mail_server = mailconfig.pop_servername
        mail_user = mailconfig.pop_username
        mail_file = mailconfig.save_mail_file
        mail_passwd = getpass.getpass("Password for {}?".format(mail_user))
        print("[PyMail email client]")
        msg_list = load_messages(mail_server, mail_user, mail_passwd)       # загрузать все
        to_delete = interact(msg_list, mail_file, mail_user, mail_passwd)
        if to_delete:
            delete_messages(mail_server, mail_user,  mail_passwd, to_delete)
    except Exception as exc:
        print("ERROR! => {}".format(exc))
    print("Bye.")
