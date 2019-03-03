"""
############################################################################
отправляет сообщения, добавляет вложения (описание и тест приводятся
в модуле __init__)
############################################################################
"""

from mailtools import mailconfig
import smtplib
import os
import mimetypes            # MIME: имя в тип
import email.utils          # Строка с датой
import email.encoders       # base64
from mailtools.mailtool import MailTool, SilentMailTool          # Импорт относительно пакета

from email.message import Message                       # Объект сообщения
from email.mime.multipart import MIMEMultipart          # Специализированиые объекты вложений
from email.mime.audio import MIMEAudio                  # с поддержкой кодирования/декодирования
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication


def fix_encode_base64(msgobj):
    """
    реализация обходного решения для ошибки в пакете email в Python 3.1,
    препятствующей созданию полного текста сообщения с двоичными частями,
    преобразованными в формат base64 или другой формат электронной почты;
    функция email.encoder, вызываемая конструктором, оставляет содержимое
    в виде строки bytes, даже при том, что оно находится в текстовом формате
    base64; это препятствует работе механизма создания полного текста
    сообщения, который предполагает получить текстовые данные и поэтому
    требует, чтобы они имели тип str;
    """
    line_len = 76        # Согласно стандартам MIME
    from email.encoders import encode_base64
    encode_base64(msgobj)           # Что обычно делает email: оставляет bytes
    text = msgobj.get_payload()     # bytes выз. ошибку в email при создании текста
    if isinstance(text, bytes):         # Декодировать в str
        text = text.decode("ascii")
    lines = []              # Разбить на строки, иначе одна большая строка
    text = text.replace('\n', '')
    while text:
        line, text = text[:line_len], text[line_len:]
        lines.append(line)
    msgobj.set_payload('\n'.join(lines))


def fix_text_required(encoding_name):
    """
    обходное решение для ошибки, вызываемой смешиванием str/bytes
    в пакете email; в Python 3.1 класс MIMEText требует передавать
    ему строки разных типов для текста в разных кодировках,
    что обусловлено преобразованием некоторых типов текста
    в разные форматы MIME;
    """
    from email.charset import Charset, QP
    charset = Charset(encoding_name)        # так email опр., что делать для кодировки
    body_enc = charset.body_encoding
    return body_enc in {None, QP}


class MailSender(MailTool):
    """
    отправляет сообщение: формирует сообщение, соединяется с SMTP-сервером;
    работает на любых компьютерах с Python+Интернет, не использует клиента
    командной строки; не выполняет аутентификацию: смотрите MailSenderAuth,
    если требуется аутентификация;
    trace_size - количество символов в трассировочном сообщении: 0=нет,
    большое значение=все;
    поддерживает кодирование Юникода для основного текста и текстовых
    частей;
    поддерживает кодирование заголовков – и полных, и компонента имени
    в адресах;
    """
    def __init__(self, smtp_server=None, trace_size=256):
        self.smtp_servername = smtp_server or mailconfig.smtp_servername
        self.trace_size = trace_size

    def send_message(self, From, To, Subj, extra_hgrs, body_text, attaches,
                     save_mail_sep="=" * 80 + "PY\n",
                     body_text_enc=mailconfig.fetch_encoding or "utf-8",
                     attaches_enc=None):
        """
        формирует и отправляет сообщение: блокирует вызывающую программу,
        в графических интерфейсах следует вызывать в отдельном потоке
        выполнения;
        body_text - основной текст, attaches - список имен файлов,
        extra_hdrs - список кортежей (имя, значение) добавляемых заголовков;
        возбуждает исключение, если отправка не удалась по каким-либо
        причинам; в случае успеха сохраняет отправленное сообщение
        в локальный файл; предполагается, что значения
        для заголовков To, Cc, Bcc являются списками
        из 1 или более уже декодированных адресов (возможно, в полном
        формате имя+<адрес>); клиент должен сам выполнять анализ,
        чтобы разбить их по разделителям или использовать
        многострочный ввод;
        обратите внимание, что SMTP допускает использование полного формата
        имя+<адрес> в адресе получателя;
        адреса Bcc теперь используются для отправки, а заголовок
        отбрасывается;
        повторяющиеся адреса получателей отбрасываются, иначе они будут
        получать несколько копий письма;
        предупреждение: не поддерживаются сообщения multipart/alternative,
        только /mixed;
        """
        # предполагается, что основной текст уже в требуемой кодировке;
        # клиенты могут декодировать, используя кодировку по выбору
        # пользователя, по умолчанию или utf8;
        # так или иначе, email требует передать либо str, либо bytes;
        if fix_text_required(body_text_enc):
            if not isinstance(body_text, str):
                body_text = body_text.decode(body_text_enc)
        else:
            if not isinstance(body_text_enc, bytes):
                body_text = body_text.encode(body_text_enc)

        # Создать корень сообщения
        if not attaches:
            msg = Message()
            msg.set_payload(body_text, charset=body_text_enc)
        else:
            msg = MIMEMultipart()
            self.add_attachments(msg, body_text, attaches, body_text_enc, attaches_enc)

        # не-ASCII заголовки кодируются; кодировать только имена
        # в адресах, иначе smtp может отвергнуть сообщение;
        # кодирует все имена в аргументе To (но не адреса),
        # предполагается, что это допустимо для сервера;
        # msg.as_string сохраняет все разрывы строк,
        # добавленные при кодировании заголовков;
        hdr_enc = mailconfig.headers_encode_to or "utf-8"           # По умолчанию utf-8
        Subj = self.encode_header(Subj, hdr_enc)                    # Полный заголовок
        From = self.encode_addr_header(From, hdr_enc)               # Имена в адресах
        To = [self.encode_addr_header(to, hdr_enc) for to in To]    # Каждый адрес
        Tos = ', '.join(To)                                         # Заголовок+аргумент

        # Добавить заголовки в корень сообщения
        msg["From"] = From
        msg["To"] = Tos                             # Возможно несколько: список адресов
        msg["Subject"] = Subj                       # серверы отвергают разделитель ';'
        msg["Date"] = email.utils.formatdate()      # Дата+время
        recip = To
        for name, value in extra_hgrs:              # Cc, Bcc, X-Mailer, etc.
            if value:
                if name.lower() not in {'cc', 'bcc'}:
                    value = self.encode_header(value, hdr_enc)
                    msg[name] = value
                else:
                    value = [self.encode_addr_header(v, hdr_enc) for v in value]
                    recip.extend(value)     # Некоторые серверы отвергают ['']
                    if name.lower() != 'bcc':               # bcc получает почту без заголовка
                        msg[name] = ', '.join(value)        # Доп. запятая между cc
        recip = list(set(recip))            # Удалить дубликаты
        full_text = msg.as_string()         # Сформировать сообщение

        # вызов sendmail возбудит исключение, если все адреса Tos ошибочны,
        # или вернет словарь с ошибочными адресами Tos
        self.trace("Sening to: {}".format(recip))
        self.trace(full_text[:self.trace_size])
        server = smtplib.SMTP_SSL(self.smtp_servername)
        self.get_password()
        self.auth_server(server)        # регистрация в подклассе
        try:
            failed = server.sendmail(From, recip, full_text)
        except smtplib.SMTPException:
            server.close()
            raise               # повтроно возбудить исключение
        else:
            server.quit()       # соединение + отправка, успех
        self.save_sent_message(full_text, save_mail_sep)
        if failed:
            class SomeAddrsFailed(Exception): pass
            raise SomeAddrsFailed("Failed addrs: {}".format(failed))
        self.trace("Sent exit")

    def add_attachments(self, main_msg, body_text, attaches,
                        body_text_enc, attaches_enc):
        """
        формирует сообщение, состоящее из нескольких частей, добавляя
        вложения attachments; использует для текста указанную кодировку
        Юникода, если была передана;
        """
        # Добавить главную часть text/plain
        msg = MIMEText(body_text, _charset=body_text_enc)
        main_msg.attach(msg)

        # Добавить части с вложениями
        encdings = attaches_enc or (['utf-8'] * len(attaches))
        for (file_name, file_enc) in zip(attaches, encdings):
            if not os.path.isfile(file_name):       # Пропустить каталоги
                continue
            # Определить тип содержимого по расширению имени файла
            # Игнорировать кодировку
            cont_type, enc = mimetypes.guess_type(file_name)
            if cont_type is None or enc is not None:            # Не определено/сжат?
                cont_type = "application/octets-stream"         # Универсалльный тип
            self.trace("Adding: {}".format(cont_type))
            # Сконструировать вложенный объект Message соответствующего типа
            maintype, subtype = cont_type.split('/', 1)
            if maintype == "text":
                if fix_text_required(file_enc):
                    data = open(file_name, 'r', encoding=file_enc)
                else:
                    data = open(file_name, 'rb')
                msg = MIMEText(data.read(), _subtype=subtype, _charset=file_enc)
                data.close()
            elif maintype == "image":
                data = open(file_name, 'rb')
                msg = MIMEImage(data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()
            elif maintype == "audio":
                data = open(file_name, 'rb')
                msg = MIMEAudio(data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()
            elif maintype == "application":
                data = open(file_name, 'rb')
                msg = MIMEApplication(data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()
            else:
                data = open(file_name, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(data.read())
                data.close()
                fix_encode_base64(msg)
            # Установить имя файла и присоденить к контейнеру
            basename = os.path.basename(file_name)
            msg.add_header("Content-Disposition", "attachment", filename=basename)
            main_msg.attach(msg)
        # Текст за пределами структуры mime, виден клиентам, которые не могут декодировать формат MIME
        main_msg.preamble = "A multi-part MIME format message.\n"
        main_msg.epilogue = ''

    def save_sent_message(self, full_text, sep):
        """
        добавляет отправленное сообщение в конец локального файла,
        если письмо было отправлено хотя бы одному адресату;
        клиент: определяет строку-разделитель, используемую приложением;
        предупреждение: пользователь может изменить файл во время работы
        сценария (маловероятно);
        """
        try:
            sentfile = open(mailconfig.sent_mail_file, 'a', encoding=mailconfig.fetch_encoding)
            if not full_text.endswith('\n'):
                full_text += '\n'
            sentfile.write(sep)
            sentfile.write(full_text)
            sentfile.close()
        except Exception as exc:
            self.trace("Could not save sent message" + str(exc))       # Не прекращает работу сценария

    def encode_header(self, hdr_text, unicode_enc="utf-8"):
        """
        кодирует содержимое заголовков с символами не из диапазона ASCII
        в соответствии со стандартами электронной почты и Юникода, применяя
        кодировку пользователя или UTF-8; метод header.encode автоматически
        добавляет разрывы строк, если необходимо;
        """
        try:
            hdr_text.encode("ascii")
        except UnicodeError:
            try:
                hdr_obj = email.header.make_header([(hdr_text, unicode_enc)])
                hdr_text = hdr_obj.encode()
            except Exception:
                pass
        return hdr_text

    def encode_addr_header(self, hdr_text, unicode_enc):
        """
        пытается закодировать имена в адресах электронной почты
        с символами не из диапазона ASCII в соответствии со стандартами
        электронной почты, MIME и Юникода; если терпит неудачу, компонент
        имени отбрасывается и используется только часть
        с фактическим адресом;
        если не может получить даже адрес, пытается декодировать целиком,
        иначе smtplib может столкнуться с ошибками, когда попытается
        закодировать все почтовое сообщение как ASCII; в большинстве случаев
        кодировки utf-8 вполне достаточно, так как она предусматривает
        довольно широкое разнообразие кодовых пунктов;
        вставляет символы перевода строки, если строка заголовка слишком
        длинная, иначе метод hdr.encode разобьет имена на несколько строк,
        но он может не замечать некоторые строки, длиннее максимального
        значения (улучшите меня); в данном случае метод Message.as_string
        форматирования не будет пытаться разбивать строки;
        смотрите также метод decodeAddrHeader в модуле mailParser,
        реализующий обратную операцию;
        """
        try:
            pairs = email.utils.getaddresses([hdr_text])        # Разбить на части
            encoded = []
            for name, addr in pairs:
                try:                            # Использовать как есть, если ascii
                    name.encode("ascii")        # Иначе закодировать компонент имени
                except UnicodeError:
                    try:
                        encoded = name.encode(unicode_enc)
                        hdr = email.header.make_header([(encoded, unicode_enc)])
                        hdr.encode()
                    except Exception:
                        name = None             # Отбросить имя, использовать только адрес
                joined = email.utils.formataddr((name, addr))
                encoded.append(joined)
            full_hdr = ', '.join(encoded)
            if len(full_hdr) > 72 or '\n' in full_hdr:
                full_hdr = ',\n'.join(encoded)
            return full_hdr
        except Exception:
            return self.encode_header(hdr_text, unicode_enc)

    def auth_server(self, server):
        return

    def get_password(self):
        pass


class MailSenderAuth(MailSender):
    """
    используется для работы с серверами, требующими аутентификацию;
    клиент: выбирает суперкласс MailSender или MailSenderAuth, опираясь
    на параметр mailconfig.smtp_user (None?)
    """
    smtp_password = None    # в классе, не в self, совместно используется всеми экземплярам

    def __init__(self, smtp_server=None, smtp_user=None, trace_size=5000):
        super(MailSenderAuth, self).__init__(smtp_server, trace_size)
        self.smtp_user = smtp_user or mailconfig.smtp_user

    def auth_server(self, server):
        server.login(self.smtp_user, self.smtp_password)

    def get_password(self):
        """
        get получает пароль для аутентификации на сервере SMTP, если он еще
        не известен; может вызываться суперклассом автоматически или
        клиентом вручную: не требуется до момента отправки, но не следует
        вызывать из потока выполнения графического интерфейса; пароль
        извлекается из файла на стороне клиента или методом подкласса
        """
        if not self.smtp_password:
            try:
                localfile = open(mailconfig.smtp_passwd_file)
                __class__.smtp_password = localfile.readline()[:-1]
                self.trace("Local file  password: {}".format(repr(self.smtp_password)))
            except Exception:
                __class__.smtp_password = self.ask_smtp_password()

    def ask_smtp_password(self):
        assert False, "Subclass must define method"


class MailSenderAuthConsole(MailSenderAuth):
    def ask_smtp_password(self):
        import getpass
        prompt = "Password for {} on {}?".format(self.smtp_user, self.smtp_servername)
        return getpass.getpass(prompt)


class SilentMailSender(SilentMailTool, MailSender):
    pass        # отключает трассировку
