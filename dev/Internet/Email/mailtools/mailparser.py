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
        """
        для текстовых клиентов возвращает первую текстовую часть в виде str;

        в содержимом простого сообщения или во всех частях составного сообщения
        отыскивает часть типа text/plain, затем text/html, затем text/*, после
        чего принимается решение об отсутствии текстовой части, пригодной для
        отображения;

        это эвристическое решение, но оно охватывает простые, а также
        multipart/alternative и multipart/mixed сообщения;

        если это не простое сообщение, текстовая часть по умолчанию имеет
        заголовок content-type со значением text/plain;

        обрабатывает вложенные сообщения, выполняя обход начиная с верхнего
        уровня, вместо сканирования списка;

        если это не составное сообщение, но имеет тип text/html, возвращает
        разметку HTML как текст типа HTML: вызывающая программа может
        открыть его в веб-броузере, извлечь простой текст и так далее;

        если это простое сообщение и текстовая часть  не найдена,
        следовательно, нет текста для отображения: предусмотрите
        сохранение/открытие содержимого в графическом интерфейсе;

        предупреждение: не пытайтесь объединить несколько встроенных
        частей типа text/plain, если они имеются;

        текстовое содержимое может иметь тип bytes - декодирует в str здесь;

        передайте as_string=False, чтобы получить разметку HTML в двоичном
        представлении для сохранения в файл;

        :param message:
        :param as_string:
        :return part_type, decoded_payload:
        """
        # отыскать простой текст
        for part in message.walk():                 # walk выполнит обход всех частей
            part_type = part.get_content_type()     # если не составное
            if part_type == "text/plain":           # может иметь формат Base64, QP, uu
                return part_type, self.decode_payload(part, as_string=as_string)
        # отыскать часть с разметкой HTML
        for part in message.walk():                 # HTML отображается вызывающей ф-цией
            part_type = part.get_content_type()
            if part == "text/html":
                return part_type, self.decode_payload(part, as_string=as_string)
        # отыскать части любого другого текстовго файла, включая XML
        for part in message.walk():
            part_type = part.get_content_type()
            if part == "text":
                return part_type, self.decode_payload(part, as_string=as_string)
        # не найдено: можно было бы использовать первую часть,
        # но она не помечена, как текстовая
        fail_text = "[No text to display]"
        if not as_string: fail_text.encode()
        return "text/plain", fail_text

    @staticmethod
    def decode_header(raw_header):
        """
        декодирует текст заголовка i18n в соответствии со стандартами
        электронной почты и Юникода и их содержимым;

        в случае ошибки при декодировании возвращает в первоначальном виде;

        клиент должен вызывать этот метод для подготовки заголовка к
        отображению: объект Message не декодируется;

        пример:
        '=?UTF-8?Q?Introducing=20Top=20Values=20..Savers?=',
        'Man where did you get that =?UTF-8?Q?assistant=3F?=';

        метод decode_header автоматически обрабатывает любые разрывы строк
        в заголовке, может возвращать несколько частей, если в заголовке
        имеется несколько подстрок, закодированных по-разному, и возвращает
        все части в виде списка строк bytes, если кодировки были найдены
        (некодированные части возвращаются как закодированные
        в raw-unicode-escape, со значением enc=None), но возвращает
        единственную часть с enc=None, которая является строкой str,
        а не bytes в Py3.x, если весь заголовок
        оказался незакодированным (должен обрабатывать смешанные типы);

        следующей реализации было бы достаточно, если бы не возможность
        появления подстрок, кодированных по-разному,
        или если бы в переменной enc не возвращалось
        значение None (возбуждает исключение, в результате
        которого аргумент raw_hdr возвращается в исходном виде):

        hdr, enc = email.header.decode_header(raw_hdr)[0]
        return hdr.decode(enc)  # ошибка, если enc=None: нет имени кодировки
                                # или кодированных подстрок

        :param raw_header:
        :return decoded_header | raw_header:
        """
        decoded = []
        try:
            parts = email.header.decode_header(raw_header)
            for (part, encoding) in parts:    # для всех подстрок заголовка
                if encoding is None:          # некодированная часть/неизвестная кодировка
                    # в случае неизвестной кодировки
                    if not isinstance(part, str): part = part.decode("raw-unicode-escape")
                else:
                    part = part.decode(encoding)
                decoded.append(part)
            return '\n'.join(decoded)       # декодированный заголовок
        except (UnicodeError, LookupError):
            return raw_header               # с декодированием не получилось

    def decode_address_header(self, raw_header):
        """
        декодирует заголовок i18n с адресами в соответствии
        со стандартами электронной почты и Юникода и их содержимым;

        должен анализировать первую часть адреса, чтобы получить
        интернационализированную часть:
        '"=?UTF-8?Q?Walmart?=" <newsletters@walmart.com>';

        заголовок From скорее всего будет содержать единственный адрес,
        но заголовки To, Cc, Bcc могут содержать несколько адресов;

        метод decode_header обрабатывает вложенные подстроки в разных
        кодировках внутри заголовка, но мы не можем напрямую вызвать
        его здесь для обработки всего заголовка, потому что он будет
        завершаться с ошибкой, если закодированная строка
        с именем будет заканчиваться кавычкой ", а не пробелом
        или концом строки; смотрите также метод encode_address_header
        в модуле mailsender, реализующий обратную операцию;

        ниже приводится первая реализация, которая терпела неудачу
        при обработке некодированных подстрок в имени и возбуждала
        исключение при встрече некодированных частей типа bytes,
        если в адресе имеется хоть одна закодированная подстрока;

        name_bytes, name_enc = email.header.decode_header(name)[0] (email+MIME)
        if name_enc: name = name_bytes.decode(name_enc)            (Юникод?)

        :param raw_header:
        :return decoded_address_header | decoded_header | raw_header:
        """
        decoded = []
        try:
            # разбить на части, учитывая запятые в адресах
            pairs = email.utils.getaddresses([raw_header])
            for (name, address) in pairs:
                try:
                    name = self.decode_header(name)
                except Exception:
                    name = None         # имя не поддается декодировке
                joined = email.utils.formataddr((name, address))
                decoded.append(joined)
            return ', '.join(decoded)   # вернуть первоначальный вид
        except Exception:
            # попробовать декодировать всю строку,
            # в случае неудачи -> исходный текст заголовка
            return self.decode_header(raw_header)

    @staticmethod
    def split_addresses(field):
        """
        используйте в графическом интерфейсе запятую как символ-разделитель
        адресов и функцию get_addresses для корректного разбиения, которая
        позволяет использовать запятые в компонентах имен адресов;

        используется программой PyMailGUI для разбиения содержимого
        заголовков To, Cc, Bcc, обработки ввода пользователя и копий
        заголовков;

        возвращает пустой список, если аргумент field пуст или возникло
        какое-либо исключение;

        :param field:
        :return addresses_list | '':
        """
        try:
            pairs = email.utils.getaddresses([field])
            return [email.utils.formataddr(pair) for pair in pairs]
        except Exception:
            return ''

    def parse_headers(self, header_text):
        """
        анализирует только заголовки, возвращает корневой объект
        email.message.Message;

        останавливается сразу после анализа заголовков, даже если
        за ними ничего не следует (команда top);

        объект email.message.Message является отображением заголовков
        сообщения;

        в качестве содержимого объекта сообщения устанавливается
        значение None, а не необработанный текст тела;

        :param header_text:
        :return parsed_headers | error_message:
        """
        parser = (email.parser.BytesHeaderParser().parsebytes
                  if isinstance(header_text, bytes)
                  else email.parser.HeaderParser().parsestr)
        try:
            return parser(header_text)
        except Exception:
            return self.error_message

    def parse_message(self, full_text):
        """
        анализирует все сообщение, возвращает корневой объект
        email.message.Message;

        содержимым объекта сообщения является строка, если is_multipart()
        возвращает False;

        при наличии нескольких частей содержимым объекта сообщения
        является множество объектов Message;

        метод, используемый здесь, действует так же, как функция
        email.message_from_string()

        :param full_text:
        :return parsed_message | error_message:
        """
        parser = (email.parser.BytesParser().parsebytes
                  if isinstance(full_text, bytes)
                  else email.parser.Parser().parsestr)
        try:
            return parser(full_text)
        except Exception:
            return self.error_message
