from mailtools import mailconfig
import smtplib
import os
import mimetypes
import email.utils
import email.encoders
import email.header

from mailtools.mailtool import MailTool, SilentMailTool
from email.encoders import encode_base64
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication


class MailSender(MailTool):
    def __init__(self, host=None, trace_size=256):
        self.host = host or mailconfig.smtp_servername
        self.trace_size = trace_size

    def send_message(self, from_, to, subj, extra_headers, body_text, attaches,
                     body_text_encoding=None, attaches_encoding=None):
        if not attaches:
            msg_obj = Message()
            msg_obj.set_payload(body_text, charset=body_text_encoding)
        else:
            msg_obj = MIMEMultipart()
            self.add_attachments(msg_obj, body_text, attaches, body_text_encoding, attaches_encoding)
        header_encoding = mailconfig.headers_encode_to or "utf-8"
        subj = self.encode_header(subj, header_encoding)
        from_ = self.encode_address_header(from_, header_encoding)
        to = [self.encode_address_header(t, header_encoding) for t in to]
        tos = ', '.join(to)
        msg_obj["From"] = from_
        msg_obj["To"] = tos
        msg_obj["Subject"] = subj
        msg_obj["Date"] = date = email.utils.formatdate(usegmt=True)
        date = date[date.find(' ')+1:date.rfind(' ')]
        date = date.replace(':', '-')
        recip = to
        for (name, value) in extra_headers:
            if value:
                if name.lower() not in {'cc', 'bcc'}:
                    value = self.encode_header(value, header_encoding)
                    msg_obj[name] = value
                else:
                    value = [self.encode_address_header(v, header_encoding) for v in value]
                    recip.extend(value)
                    if name.lower != 'bcc':
                        msg_obj[name] = ', '.join(value)
        recip = list(set(recip))
        full_text = msg_obj.as_string()

        self.trace("Sending to:".format(recip))
        self.trace(full_text[:self.trace_size])
        server = smtplib.SMTP_SSL(self.host)
        self.get_password()
        self.authenticate_server(server)
        try:
            failed = server.sendmail(from_, recip, full_text)
        except smtplib.SMTPException:
            server.close()
            raise
        else:
            server.quit()
        self.save_sent_message(full_text, date, '; '.join(to))
        if failed:
            class SomeAddressesFailed(Exception):
                pass
            raise SomeAddressesFailed("Failed addresses: {}".format(failed))
        self.trace("Sent exit")

    def add_attachments(self, main_msg, body_text, attaches,
                        body_text_encoding, attaches_encoding):
        msg = MIMEText(body_text, _charset=body_text_encoding)
        main_msg.attach(msg)
        encodings = attaches_encoding or (['utf-8'] * len(attaches))
        for (file_name, file_enc) in zip(attaches, encodings):
            if not os.path.isfile(file_name):
                continue
            cont_type, encoding = mimetypes.guess_type(file_name)
            if cont_type is None or encoding is not None:
                cont_type = "application/octets-stream"
            self.trace("Attaching: {}".format(cont_type))
            maintype, subtype = cont_type.split('/', 1)
            if maintype == "text":
                if encoding:
                    args = dict(mode='r', encoding=file_enc)
                else:
                    args = dict(mode='rb')
                with open(file_name, **args) as data:
                    msg = MIMEText(data.read(), _subtype=subtype, _charset=file_enc)
            elif maintype == "image":
                with open(file_name, 'rb') as data:
                    msg = MIMEImage(data.read(), _subtype=subtype)
            elif maintype == "audio":
                with open(file_name, 'rb') as data:
                    msg = MIMEAudio(data.read(), _subtype=subtype)
            elif maintype == "application":
                with open(file_name, 'rb') as data:
                    msg = MIMEApplication(data.read(), _subtype=subtype)
            else:
                with open(file_name, 'rb') as data:
                    msg = MIMEBase(maintype, subtype)
                    msg.set_payload(data.read())
                    encode_base64(msg)
            basename = os.path.basename(file_name)
            msg.add_header("Content-Disposition", "attachment", filename=basename)
            main_msg.attach(msg)
        main_msg.preamble = "A multipart MIME format message.\n"
        main_msg.epilogue = ""

    def save_sent_message(self, full_text, date, recipients):
        filename = "{} {}.txt".format(date, recipients)
        path = mailconfig.save_mail_dir
        if not os.path.exists(path):
            os.mkdir(path)
        filename.replace(' ', '_')
        fullname = os.path.join(path, filename)
        try:
            with open(fullname, 'w') as sent_file:
                if not full_text.endswith('\n'):
                    full_text += '\n'
                for line in full_text:
                    sent_file.write(line)
        except Exception as exc:
            self.trace("Couldn't save sent message: {}".format(exc))

    @staticmethod
    def encode_header(header_text, unicode_encode="utf-8"):
        try:
            header_text.encode("ascii")
        except UnicodeError:
            try:
                header_obj = email.header.make_header([(header_text, unicode_encode)])
                header_text = header_obj.encode()
            except Exception:
                pass
        return header_text

    def encode_address_header(self, header_text, unicode_encoding):
        try:
            pairs = email.utils.getaddresses([header_text])
            encoded = []
            for (name, address) in pairs:
                try:
                    name.encode("ascii")
                except UnicodeError:
                    try:
                        unicode = name.encode(unicode_encoding)
                        header_obj = email.header.make_header([(unicode, unicode_encoding)])
                        header_obj.encode()
                    except Exception:
                        name = None
                joined = email.utils.formataddr((name, address))
                encoded.append(joined)
            full_header = ', '.join(encoded)
            if len(full_header) > 72 or '\n' in full_header:
                full_header = ',\n'.join(encoded)
            return full_header
        except Exception:
            return self.encode_header(header_text, unicode_encoding)

    def authenticate_server(self, server):
        raise NotImplementedError

    def get_password(self):
        raise NotImplementedError


class MailSenderAuth(MailSender):
    def __init__(self, host=None, user=None, trace_size=5000):
        super(MailSenderAuth, self).__init__(host, trace_size)
        self.user = user or mailconfig.smtp_user
        self.password = None

    def authenticate_server(self, server):
        try:
            print(self.user, self.password)
            server.login(self.user, self.password)
        except smtplib.SMTPAuthenticationError:
            self.trace("Invalid name or password! Check your settings in file: {}".format(mailconfig.__file__))

    def get_password(self):
        if self.password:
            return self.password
        try:
            pswd_file = open(mailconfig.smtp_passwd_file)
            self.password = pswd_file.readline()[:-1]
            self.trace("Local file password")
        except Exception:
            self.password = "mr.Hedgehognumber1"#self.ask_password()

    def ask_password(self):
        raise NotImplementedError


class MailSenderAuthConsole(MailSenderAuth):
    def ask_password(self):
        import getpass
        prompt = "Password for {} on {}?".format(self.user, self.host)
        return getpass.getpass(prompt)


class SilentMailSender(SilentMailTool, MailSender):
    def get_password(self): pass

    def authenticate_server(self, server): pass
