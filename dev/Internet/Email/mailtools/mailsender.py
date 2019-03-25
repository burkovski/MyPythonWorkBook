from mailtools import mailconfig
import smtplib
import os
import mimetypes         # MIME: имя в тип
import email.utils       # строка с датой
# import email.encoders
import email.header

from mailtools.mailtool import MailTool, SilentMailTool
from email.encoders import encode_base64          # декодер base64
from email.message import Message                 # корневой объект сообщения
from email.mime.multipart import MIMEMultipart    # специализированые объекты вложений
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication


class MailSenderSendError(Exception):
    pass


class MailSenderConnectError(Exception):
    pass


class MailSenderAddressFailed(Exception):
    pass


class MailSenderAuthError(Exception):
    pass


class MailSender(MailTool):
    # свойство класса, используется для того, чтобы
    # определить момент вывода сообщения о успешной авторизации
    _auth = False

    def __init__(self, host=None, ssl=True, trace_size=256):
        self.host       = host or mailconfig.smtp_servername
        self.__ssl      = ssl
        self.trace_size = trace_size

    def connect(self):
        """
        соединяется с сервером SMTP, по адресу, сохраненному
        в свойстве host;

        использует SSL по умолчанию, для "обычного" поключения -
        передать в параметр ssl=False;

        не запрашивает у пользователя пароль и не проводит аутентификацию;

        :return server:
        """
        self.trace("Connecting...")
        conn_type = (smtplib.SMTP_SSL if self.__ssl     # использовать SSL?
                     else smtplib.SMTP)
        try:
            server = conn_type(self.host)       # Соединиться с сервером по заданому адресу
        # некорректный адрес сервера?
        except Exception:                       # Повтороное исключение с сообщением об ошибке
            raise MailSenderConnectError(
                "Invalid host name or expected/unexpected SSL-mode. "
                "Check your settings in file: <{}>".format(mailconfig.__file__)
            )
        else:
            if not self._auth: self.trace("Connected successfully.")
            return server

    def disconnect(self, server):
        """
        разрывает соединение с сервером, закрывает текущий почтовый ящик.

        :param server:
        """
        server.quit()
        self.trace("Disconnected.")

    def send_message(self, *, from_hdr, to_list, subj_hdr, extra_headers, body_text,
                     attaches=None, body_text_encoding=None, attaches_encoding=None):
        """
        отправляет сообщение: формирует сообщение, соединяется с SMTP сервером;

        работает на любых компьютерах с Python+Интернет, не использует клиент
        командной строки;

        не выполняет аутентификацию: смотрите MailSenderAuth, если требуется
        аутентификация;

        trace_size - количество символов в трассировочном сообщении: 0=нет,
        большее значение=все;

        поддерживает кодирование Юникода для основного текста и текстовых
        частей;

        поддерживает кодирование заголовков – и полных, и компонента имени
        в адресах;

        :param from_hdr:
        :param to_list:
        :param subj_hdr:
        :param extra_headers:
        :param body_text:
        :param attaches:
        :param body_text_encoding:
        :param attaches_encoding:
        :return None:
        """
        # создать корень сообщения
        if not attaches:
            msg_obj = Message()
            msg_obj.set_payload(body_text, charset=body_text_encoding)
        else:
            msg_obj = MIMEMultipart()
            self.add_attachments(msg_obj, body_text, attaches, body_text_encoding, attaches_encoding)
        # не-ASCII заголовки кодируются; кодировать только имена
        # в адресах, иначе smtp может отвергнуть сообщение;
        # кодирует все имена в аргументе To (но не адреса),
        # предполагается, что это допустимо для сервера;
        # msg.as_string сохраняет все разрывы строк,
        # добавленные при кодировании заголовков;
        header_encoding = mailconfig.headers_encode_to or "utf-8"
        subj_hdr = self.encode_header(subj_hdr, header_encoding)
        from_hdr = self.encode_address_header(from_hdr, header_encoding)
        to_list  = [self.encode_address_header(to, header_encoding)
                    for to in to_list]
        to_hdr   = ', '.join(to_list)
        date_hdr = email.utils.formatdate(usegmt=True)
        # добавим заголовки
        msg_obj["From"]    = from_hdr
        msg_obj["To"]      = to_hdr
        msg_obj["Subject"] = subj_hdr
        msg_obj["Date"]    = date_hdr
        # реформат даты, используется как часть имени файла, при сохранении
        # получить только дату <DD MM YYYY HH:MM:SS>
        date = date_hdr[date_hdr.fetch_some(' ') + 1:date_hdr.rfind(' ')]
        date = date.replace(':', '-')                    # двоеточие недопустимо в имени файла
        # все получатели: [to + cc + bcc]
        recipients = set(to_list)           # set - повторы нам ни к чему...
        # X-Mailer, Cc, Bcc, etc.
        # raise MailSenderAddressFailed(extra_headers)
        for (name, value) in extra_headers:
            if value:
                if name.lower() in {'cc', 'bcc'}:    # имеются получатели копии/скрытой копии?
                    value = tuple(self.encode_address_header(v, header_encoding)
                                  for v in value)         # закодировать имена получателей
                    # заголовка bcc быть не должно!
                    # эти адреса - только в списке получателей
                    if name.lower() != 'bcc':
                        msg_obj[name] = ', '.join(value)
                    recipients.add(value)
                else:   # остальные экстра-хедес - закодировать -> добавить
                    value = self.encode_header(value, header_encoding)
                    msg_obj[name] = value
        # получить полный текст сконструированого сообщения
        full_text = msg_obj.as_string()
        self.trace("Sending to:".format(recipients))
        self.trace(full_text[:self.trace_size])
        server = self.connect()
        try:
            # в случае неуспешной отпраки - dict или подкласс SMTPException
            failed = server.sendmail(from_hdr, recipients, full_text)
            # MailSenderAddressFailed(Exception) - в иерархии выше, чем
            # SMTPException(OSError) -> это исключение не будет перехвачено
            if failed: raise MailSenderAddressFailed()
            self.trace("Mail was sent")
        except smtplib.SMTPException as exc:
            raise MailSenderSendError("Mail send error: {}".format(exc))
        finally:
            self.disconnect(server)     # дисконнект - в любом случае
        # напоследок - сохранить сообщение
        self.save_sent_message(full_text, date, '; '.join(to_list))
        self.trace("Sent exit")

    def define_params(self, file_name, file_enc):
        """
        по полученому имени файла определяет: словарь с параметрами для
        открытия этого файла, тип вложенного объекта Message соотвествующего
        типа, словарь с параметрами для создания вложеного объекта;

        :param file_name:
        :param file_enc:
        :return file_params, mime_type, mime_params:
        """
        # определить тип содержимого по расширению файла
        # игнорировать кодировку
        cont_type, encoding = mimetypes.guess_type(file_name)
        if cont_type is None or encoding is not None:  # не определено/сжат
            cont_type = "application/octets-stream"  # универсальный тип
        self.trace("Attaching: {}".format(cont_type))
        # сконструировать вложенный объект Message, соотвествующего типа
        maintype, subtype = cont_type.split('/', 1)     # тип/подтип
        # параматры по умолчанию
        file_params = dict(mode='rb')
        mime_params = dict(_subtype=subtype)
        if maintype == "text":
            # текстовый файл -> текстовый режим + кодировка
            file_params.update(mode='r', encoding=file_enc)
            mime_type = MIMEText
            # добавить информацию о кодировке
            mime_params.update(_charset=file_enc)
        elif maintype == "image":
            mime_type = MIMEImage
        elif maintype == "audio":
            mime_type = MIMEAudio
        elif maintype == "application":
            mime_type = MIMEApplication
        else:
            mime_type = MIMEBase       # остальные -> добавить инфо о типе файла
            mime_params.update(_maintype=maintype)
        return file_params, mime_type, mime_params

    def add_attachments(self, main_msg, body_text, attaches,
                        body_text_encoding, attaches_encoding):
        """
        формирует сообщение, состоящее из нескольких частей, добавляя
        вложения attachments;

        использует для текста указанную кодировку Юникода, если была
        передана;

        :param main_msg:
        :param body_text:
        :param attaches:
        :param body_text_encoding:
        :param attaches_encoding:
        :return:
        """
        # добавть главную часть text/plain
        msg = MIMEText(body_text, _charset=body_text_encoding)
        main_msg.attach(msg)
        # добавить части с вложениями
        encodings = attaches_encoding + ([None] * (len(attaches) - len(attaches_encoding)))
        self.trace(encodings)
        for (file_name, file_enc) in zip(attaches, encodings):
            self.trace(file_name)
            if not os.path.isfile(file_name):
                continue    # пропустить каталоги
            # определить требуемый тип объекта и параметы
            file_params, mime_type, mime_params = self.define_params(file_name, file_enc)
            with open(file_name, **file_params) as attachment:
                if mime_type is MIMEBase:
                    # MIMEBase - подкласс email.Message, в котором аргумент data
                    # не предусмотрен -> содержимое аттачмента присоеденить с
                    # с помошью set_payload(data) и закодировать в base64 вручную
                    msg = mime_type(**mime_params)
                    msg.set_payload(attachment.read())
                    encode_base64(msg)
                else:
                    # здесь первый аргумент - data
                    msg = mime_type(attachment.read(), **mime_params)
            # определить имя файла без пути
            basename = os.path.basename(file_name)
            # добавить соотествующий заголовок
            msg.add_header("Content-Disposition", "attachment", filename=basename)
            # присоеденить к контейнеру
            main_msg.attach(msg)
        main_msg.preamble = "A multipart MIME format message.\n"
        main_msg.epilogue = ""

    def save_sent_message(self, full_text, date, recipients):
        """
        добавляет файл с текстом отправленного сообщения в директорию
        mailconfig.save_mail_dir, если письмо было отправлено хотя бы
        одному адресату;

        в качестве имени файла используется пара дата+получатели;

        :param full_text:
        :param date:
        :param recipients:
        :return None:
        """
        filename = "{} {}.txt".format(date, recipients)       # имя файла
        filename.replace(' ', '_')                              # пробелы ни к чему
        path = mailconfig.save_mail_dir                         # директория
        if not os.path.exists(path):        # не существует? - создадим!
            os.mkdir(path)
        fullname = os.path.join(path, filename)         # полное имя файла
        try:
            with open(fullname, 'w', encoding=mailconfig.save_mail_encoding) as sent_file:
                if not full_text.endswith('\n'):
                    full_text += '\n'
                for line in full_text:
                    sent_file.write(line)
        except Exception as exc:
            self.trace("Couldn't save sent message: {}".format(exc))
            raise

    @staticmethod
    def encode_header(header_text, unicode_encode="utf-8"):
        """
        кодирует содержимое заголовков с символами не из диапазона ASCII
        в соответствии со стандартами электронной почты и Юникода, применяя
        кодировку пользователя или UTF-8;

        метод header.encode автоматически добавляет разрывы строк, если необходимо;

        :param header_text:
        :param unicode_encode:
        :return:
        """
        try:
            header_text.encode("ascii")     # а вдруг не юникод?
        except UnicodeError:                # юникод!
            try:
                # make_header ждет пары (текст_заголовка, кодировка)
                header_obj = email.header.make_header([(header_text, unicode_encode)])
                header_text = header_obj.encode()       # кодирует юникод по стандарту RFC
            except Exception:
                pass
        return header_text

    def encode_address_header(self, header_text, unicode_encoding):
        """
        пытается закодировать имена в адресах электронной почты
        с символами не из диапазона ASCII в соответствии со стандартами
        электронной почты, MIME и Юникода;

        если терпит неудачу, компонент имени отбрасывается и используется
        только часть с фактическим адресом;

        если не может получить даже адрес, пытается декодировать целиком,
        иначе smtplib может столкнуться с ошибками, когда попытается
        закодировать все почтовое сообщение как ASCII;

        в большинстве случаев
        кодировки utf-8 вполне достаточно, так как она предусматривает
        довольно широкое разнообразие кодовых пунктов;

        вставляет символы перевода строки, если строка заголовка слишком
        длинная, иначе метод hdr.encode разобьет имена на несколько строк,
        но он может не замечать некоторые строки, длиннее максимального
        значения (улучшите меня);

        в данном случае метод Message.as_string форматирования не будет
        пытаться разбивать строки;

        смотрите также метод decode_address_header в модуле mailparser,
        реализующий обратную операцию;

        :param header_text:
        :param unicode_encoding:
        :return:
        """
        try:
            pairs = email.utils.getaddresses([header_text])     # разбить на части
            encoded = []
            for (name, address) in pairs:
                try:                            # использовать как есть, если ascii
                    name.encode("ascii")        # иначе закодировать компонент имени
                except UnicodeError:
                    try:
                        unicode = name.encode(unicode_encoding)
                        header_obj = email.header.make_header([(unicode, unicode_encoding)])
                        header_obj.encode()
                    except Exception:
                        name = None         # отбросить имя - использовать только адрес
                joined = email.utils.formataddr((name, address))
                encoded.append(joined)
            full_header = ', '.join(encoded)
            if len(full_header) > 72 or '\n' in full_header:
                full_header = ',\n'.join(encoded)
            return full_header
        except Exception:
            return self.encode_header(header_text, unicode_encoding)

    def get_password(self):
        raise NotImplementedError


class MailSenderAuth(MailSender):
    _auth = True    # этот класс проводит аутентификацию

    def __init__(self, host=None, ssl=True, trace_size=5000):
        super(MailSenderAuth, self).__init__(host, ssl, trace_size)
        self.user = mailconfig.smtp_username    # имя из конфига
        self.password = None                    # пароль изначально неизвестен

    def connect(self):
        """
        соединяется с сервером SMTP, по адресу, сохраненному
        в свойстве host, проводит авторизацию;

        использует SSL по умолчанию, для "обычного" поключения -
        передать в параметр ssl=False;

        запрашивает у пользователя пароль и проводит аутентификацию;

        если авторизация была успешена, сохраняет пароль
        для последующих подключений;

        в случае ошибки авторизации или, если сервер не поддерживает
        авторизацию - возбуждает исключение для обработки вызывающей
        программой.

        :return server:
        """
        # получить объект сервера и провести авторизацию
        server = super(MailSenderAuth, self).connect()
        password = self.get_password()              # Файл | GUI | консоль | web-интерфейс | прочее
        try:
            if not all((self.user, password)):
                raise Exception("password: [{}]\nuser: [{}]".format(self.password, self.user))
            server.login(self.user, password)       # Зарегистрироваться на сервере
        except smtplib.SMTPAuthenticationError:     # В случае ошибки авторизации
            raise MailSenderAuthError("Invalid name or password! "
                                      "Check your settings in file: <{}>"
                                      .format(mailconfig.__file__))
        except smtplib.SMTPNotSupportedError:       # Если сервер не поддерживает авторизацию
            raise MailSenderAuthError("Server {} not supported authentication."
                                      "You should use MailSender".format(self.host))
        else:
            prompt = "Connected successfully."
            if not self.password:
                self.password = password      # Валидный пароль -> сохранить для последующих подключений
                prompt += " Greetings <{}>!".format(self.user)
            self.trace(prompt)
            return server

    def get_password(self):
        """
        получает пароль для пользователя на указаном сервере,
        если он еще не известен, иначе - возвращает его;

        :return password:
        """
        if self.password:  # если пароль известен -> вернуть его вызывающему
            return self.password
        try:
            # попробовать прочитать пароль из файла, если таковой имеется
            with open(mailconfig.imap_password_file) as pswd_file:
                self.password = pswd_file.readline()[:-1]
                self.trace("Password from local file {}".format(mailconfig.imap_password_file))
        except (FileNotFoundError, TypeError):
            # запросить пароль у пользователя
            return self.ask_password()

    def ask_password(self):
        raise NotImplementedError


class MailSenderAuthConsole(MailSenderAuth):
    """
    класс, для использования в консоли
    """
    def ask_password(self):
        import getpass
        prompt = "Password for {} on {}? ".format(self.user, self.host)
        return getpass.getpass(prompt)


class SilentMailSenderAuth(SilentMailTool, MailSenderAuth):
    """
    проводит аутентификацию, отключает трассировку
    """
    def ask_password(self):
        pass


class SilentMailSender(SilentMailTool, MailSender):
    """
    отключает трассировку
    """
    def get_password(self):
        pass
