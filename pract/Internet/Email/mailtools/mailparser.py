import os
import mimetypes        # mime: отображение текста в имя
import sys
import email.parser     # Анализ текста в объекте Message
import email.header     # Кодирование/декордирование заголовков
import email.utils      # Кодирование/декордирование заголовков с адресами

from email.message import Message
from mailtools.mailtool import MailTool


class MailParser(MailTool):
    """
    методы анализа текста сообщения, вложений

    важное замечание: содержимое объекта Message может быть простой строкой
    в простых несоставных сообщениях или списком объектов Message
    в сообщениях, состоящих из нескольких частей (возможно, вложенных);

    мы не будем различать эти два случая, потому что генератор walk
    объекта Message всегда первым возвращает сам объект и прекрасно
    обрабатывает простые, несоставные объекты
    (выполняется обход единственного объекта);

    в случае простых сообщений тело сообщения всегда рассматривается здесь
    как единственная часть сообщения;

    в случае составных сообщений список
    частей включает основной текст сообщения, а также все вложения;

    это позволяет обрабатывать в графических интерфейсах простые нетекстовые
    сообщения как вложения (например, сохранять, открывать);

    иногда, в редких случаях, содержимым частей объекта Message
    может быть None;

    добавлена поддержка автоматического декодирования заголовков
    сообщения в соответствии с их содержимым - как полных заголовков,
    таких как Subject, так и компонентов имен в заголовках
    с адресами, таких как From и To;

    клиент должен запрашивать эту операцию после анализа полного
    текста сообщения, перед отображением: механизм анализа
    не выполняет декодирование;
    """

    error_message = Message()
    error_message.set_payload("[Unable to parse message - format error]")

    def walk_named_parts(self, message):
        """
        функция-генератор, позволяющая избежать повторения логики выбора
        именованных частей;

        пропускает заголовки multipart, извлекает
        имена файлов частей;

        message – это уже созданный из сообщения
        объект email.message.Message;

        не пропускает части необычного типа:
        содержимым может быть None, при сохранении следует обрабатывать
        такую возможность;

        некоторые части некоторых других типов также
        может потребоваться пропустить;
        """
        for (ix, part) in enumerate(message.walk()):        # walk включает сообщение
            full_type = part.get_content_type()             # ix включает пропущенные части
            main_type = part.get_content_maintype()
            if main_type == "multipart":                    # multipart/* -> контейнер
                continue
            elif full_type == "message/rfc822":             # Пропустить message/rfc822
                continue
            else:
                file_name, cont_type = self.part_name(part, ix)
                yield (file_name, cont_type, part)

    @staticmethod
    def part_name(part, ix):
        """
        извлекает имя файла и тип содержимого из части сообщения;

        имя файла: сначала пытается определить из параметра
        filename заголовка Content-Disposition, затем из параметра name
        заголовка Content-Type и под конец генерирует имя файла из типа,
        определяемого с помощью модуля mimetypes;

        :param part:
        :param ix:
        :return file_name, cont_type:
        """
        filename = part.get_filename()           # имя файла в заголовке
        cont_type = part.get_content_type()      # maintype/subtype
        if not filename:
            filename = part.get_param("name")    # Проверить параметр name
        if not filename:                         # заголовка content-type
            if cont_type == "text/plain":        # Расширение текстового файла
                ext = ".txt"                     # Иначе будет предложено .ksh!
            else:
                ext = mimetypes.guess_extension(cont_type)
                if not ext: ext = ".bin"         # Универсальное по умолчанию
            filename = "part-{0:03}{1}".format(ix, ext)
        return filename, cont_type

    def save_parts(self, save_dir, message):
        """
        сохраняет все части сообщения в файлах в локальном каталоге;

        возвращает список [('тип/подтип, 'имя файла')] для использования
        в вызывающей программе, но не открывает какие-либо части или
        вложения;

        метод get_payload декодирует содержимое с применением
        кодировок base64, quoted-printable, uuencoded; механизм анализа
        почтовых сообщений может вернуть содержимое None для некоторых
        необычных типов частей, которые, вероятно, следует пропустить:
        здесь преобразовать в str для безопасности;

        :param save_dir:
        :param message:
        :return part_files:
        """
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        part_files = []
        for (filename, cont_type, part) in self.walk_named_parts(message):
            fullname = os.path.join(save_dir, filename)
            content = part.get_payload(decode=True)         # Декодирует base64, QP, uu
            if not isinstance(content, bytes):
                content = b"(no content)"
            with open(fullname, 'wb') as file_obj:          # Двоичный режим
                file_obj.write(content)
            part_files.append((cont_type, fullname))        # Для открытия в вызывающей программе
        return part_files

    def save_one_part(self, save_dir, part_name, message):
        """
        То же самое, но отыскивает по имени только одну часть
        и сохраняет ее

        :param save_dir:
        :param part_name:
        :param message:
        :return:
        """
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        fullname = os.path.join(save_dir, part_name)
        cont_type, content = self.find_one_part(part_name, message)
        if not isinstance(content, bytes):
            content = b"(no content)"
        with open(fullname, 'wb') as file_obj:
            file_obj.write(content)
        return cont_type, fullname

    def parts_list(self, message):
        """
        возвращает список имен файлов для всех частей уже
        проанализированного сообщения, используется та же логика определения
        имени файла, что и в save_parts, но не сохраняет части в файлы;

        :param message:
        :return parts_list:
        """
        return [filename for (filename, cont_type, part)
                in self.walk_named_parts(message)]

    def find_one_part(self, part_name, message):
        """
        отыскивает и возвращает содержимое части по ее имени;

        предназначен для совместного использования с методом partsList;

        можно было бы также использовать mimetypes.guess_type(part_name);

        необходимости поиска можно было бы избежать, сохраняя данные
        в словаре;

        содержимое может иметь тип str или bytes - преобразовать
        при необходимости;

        :param part_name:
        :param message:
        :return:
        """
        for (filename, cont_type, part) in self.walk_named_parts(message):
            if filename == part_name:
                content = part.get_payload(decode=True)
                return cont_type, content

    @staticmethod
    def decode_payload(part, *, as_string=True):
        """
        декодирует текстовую часть, представленную в виде
        строки bytes, в строку str Юникода для отображения,
        разбиения на строки и так далее;

        аргумент part - это объект Message;

        (decode=1) декодирует из формата MIME (base64, uuencode, qp), bytes.decode()
        выполняет дополнительное декодирование в текстовые строки Юникода;

        прежде чем вернуть строку с ошибкой, сначала пытается применить
        кодировку, указанную в заголовках сообщения (если имеется
        и соответствует), затем пытается применить кодировку по умолчанию
        для текущей платформы и несколько предполагаемых кодировок;

        :param part:
        :param as_string:
        :return:
        """
        payload = part.get_payload(decode=True)         # bytes
        if as_string and isinstance(payload, bytes):
            encodings = set()
            hdr_enc = part.get_content_charset()        # Сначала проверить заголовки сообщения
            if hdr_enc: encodings.add(hdr_enc)
            encodings.add(sys.getdefaultencoding())
            encodings.update(("latin-1", "utf-8"))
            for encoding in encodings:
                try:
                    payload = payload.decode(encoding)
                    break
                except (UnicodeError, LookupError):
                    pass
            else:
                payload = "--Sorry! Cannot decode Unicode text--"
        return payload

    def find_main_text(self, message, *, as_string=True):
        for part in message.walk():
            part_type = part.get_content_type()
            if part_type == "text/plain":
                return part_type, self.decode_payload(part, as_string=as_string)

        for part in message.walk():
            part_type = part.get_content_type()
            if part == "text/html":
                return part_type, self.decode_payload(part, as_string=as_string)

        for part in message.walk():
            part_type = part.get_content_type()
            if part == "text":
                return part_type, self.decode_payload(part, as_string=as_string)

        fail_text = "[No text to display]"
        if not as_string:
            fail_text.encode()
        return "text/plain", fail_text

    @staticmethod
    def decode_header(raw_header):
        decoded = []
        try:
            parts = email.header.decode_header(raw_header)
            for (part, encoding) in parts:
                if encoding is None:
                    if not isinstance(part, str):
                        part = part.decode("raw-unicode-escape")
                else:
                    part = part.decode(encoding)
                decoded.append(part)
            return '\n'.join(decoded)
        except (UnicodeError, LookupError):
            return raw_header

    def decode_address_header(self, raw_header):
        decoded = []
        try:
            pairs = email.utils.getaddresses([raw_header])
            for (name, address) in pairs:
                try:
                    name = self.decode_header(name)
                except Exception:
                    name = None
                joined = email.utils.formataddr((name, address))
                decoded.append(joined)
            return ', '.join(decoded)
        except Exception:
            return self.decode_header(raw_header)

    @staticmethod
    def split_addresses(field):
        try:
            pairs = email.utils.getaddresses([field])
            return [email.utils.formataddr(pair) for pair in pairs]
        except Exception:
            return ''

    def parse_headers(self, mail_text):
        try:
            return email.parser.Parser().parsestr(mail_text, headersonly=True)
        except Exception:
            return self.error_message

    def parse_message(self, full_text):
        try:
            return email.parser.BytesParser().parsebytes(full_text)
        except Exception:
            return self.error_message

    def parse_message_raw(self, full_text):
        try:
            return email.parser.HeaderParser().parsestr(full_text)
        except Exception:
            return self.error_message
