import imaplib
import sys

from mailtools import mailconfig
from mailtools.mailtool import MailTool, SilentMailTool


# Ошибка авторизации: неверное имя сервера, пользователя или пароль
class MailFetcherAuthError(Exception):
    pass


class MailFetcherSyncError(Exception):
    pass


class MailFetcher(MailTool):
    """
    получение почты: соединяется, извлекает заголовки+содержимое, удаляет;
    есть возможность выбора: извлечь все сообщения или непрочитаные;
    работает на любых компьютерах с Python+Интернет;
    предусматривает декодирование полного текста сообщений
    для последующей передачи его механизму анализа;
    """

    # Параметры uid-запроса поиска:
    __search_unseen = "UNSEEN"                      # только непрочитанные
    __search_all    = "ALL"                         # всех сообщений
    # Параметры uid-запроса извлечения:
    __fetch_header  = "(RFC822.HEADER)"             # только заголовок
    __fetch_full    = "(RFC822)"                    # сообщение целиком

    def __init__(self, host=mailconfig.imap_servername, ssl=True):
        self.host           = host                         # DNS адрес сервера
        self.ssl_conn       = ssl                          # SSL-mode
        self.user           = mailconfig.imap_username     # Имя пользователя
        self.__password     = None                         # Если None -> запросить пароль
        self.fetch_encoding = mailconfig.fetch_encoding    # Кодировка для извлечения
        self.fetch_limit    = mailconfig.fetch_limit       # Лимит извлекаемых сообщений

    def connect(self):
        """
        соединяется с сервером IMAP, по адресу, сохраненному
        в свойстве host;

        использует SSL по умолчанию, для "обычного" поключения -
        передать в параметр ssl=False;

        запрашивает у пользователя пароль и проводит аутентификацию;

        если авторизация была успешена, сохраняет пароль
        для последующих подключений;

        проводит выбор ящика входящих сообщений;

        в случае ошибки авторизации - возбуждает исключение
        для обработки вызывающей программой.

        :return server:
        """
        self.trace("Connecting...")
        password = self.get_password()                      # Файл | GUI | консоль | web-интерфейс | прочее
        conn_type = (imaplib.IMAP4_SSL if self.ssl_conn     # использовать SSL?
                     else imaplib.IMAP4)
        try:
            server = conn_type(self.host)        # Соединиться с сервером по заданому адресу
            server.login(self.user, password)    # Зарегистрироваться на сервере
        except Exception:                        # В случае ошибки авторизации
            raise MailFetcherAuthError(          # Повтороное исключение с сообщением об ошибке
                "Invalid name or password! Check your settings in file: <{}>".format(mailconfig.__file__)
            )
        else:
            prompt = "Connected successfully."
            if not self.__password:
                prompt += " Greetings <{}>!".format(self.user)
            self.trace(prompt)
            server.select(mailbox="INBOX")
            self.__password = password        # Валидный пароль -> сохранить для последующих подключений
            return server

    def disconnect(self, server):
        """
        разрывает соединение с сервером, закрывает текущий почтовый ящик.

        :param server:
        """
        server.close()
        server.logout()
        self.trace("Disconnected.")

    @staticmethod
    def nums_to_uids(server):
        """
        Возвращает словарь вида: {номер сообщения: uid} для полученного объекта сервера;

        В случае отличающейся длины списков номеро и uid(рассинхронизация), возбуждает исключение.

        :param server:
        :return:
        """
        msg_nums = server.search(None, "ALL")[1][0].split()             # Список всех номеров
        msg_uids = server.uid("SEARCH", None, "ALL")[1][0].split()      # Список всех uid
        if len(msg_nums) != len(msg_uids):                              # Рассинхрон?
            raise MailFetcherSyncError("Different nums and uids len")
        return {num: uid for (num, uid) in zip(msg_nums, msg_uids)}

    @staticmethod
    def decode_full_text(msg_bytes):
        """
        декодирует полный текст сообщения, представленный в виде
        строки bytes, в строку Юникода str;

        выполняется на этапе получения
        для последующего отображения или анализа (после этого полный текст
        почтового сообщения всегда будет обрабатываться как строка Юникода);

        декодирование выполняется в соответствии с настройками в классе или
        в экземпляре или применяются наиболее распространенные кодировки;

        можно было бы также попробовать определить кодировку из заголовков
        или угадать ее, проанализировав структуру байтов;

        для большинства сообщений достаточно будет простой 8-битовой
        кодировки, такой как latin-1, потому что стандартной считается
        кодировка ASCII;

        этот метод применяется ко всему тексту сообщения -
        это лишь один из этапов на пути декодирования сообщений: содержимое
        и заголовки сообщений могут также находиться в формате MIME и быть
        закодированы в соответствии со стандартами электронной почты
        и Юникода; смотрите реализацию модулей mailparser и mailsender;

        :param msg_bytes:
        :return text:
        """
        text = None
        kinds = {"utf-8"}
        kinds.update(("ascii", "latin-1"))
        kinds.add(sys.getdefaultencoding())
        for kind in kinds:
            try:
                text = [line.decode(kind) for line in msg_bytes.splitlines()]
                break
            except (UnicodeError, LookupError):
                continue
        if text is None:
            blank_line = msg_bytes.index(b'')
            headers_only = msg_bytes[:blank_line]
            for kind in kinds:
                try:
                    text = [line.decode(kind) for line in headers_only]
                    break
                except UnicodeError:
                    pass
            else:
                text = ["From: (sender of unknown Unicode format headers)"]
            text.extend(('', "--Sorry: mailtools cannot decode this mail content!"))
        return text

    def download_message(self, msg_uid, *, server=None, decode=False, prompt=None):
        """
        загружает полный текст одного сообщения по указанному uid,
        анализ содержимого выполняет вызывающая программа.

        :param msg_uid:
        :param server:
        :param decode:
        :param prompt:
        :return msg:
        """
        if not prompt: prompt = "uid={}".format(int(msg_uid))
        self.trace("Loading message: {}".format(prompt))
        if not server:                  # Если вызывается как отдельный метод ->
            server = self.connect()     # установить соединение
        try:
            status, msg_data = server.uid("FETCH", msg_uid, self.__fetch_full)    # Извлечь сообщение
            msg = msg_data[0][1]
            if decode: msg = '\n'.join(self.decode_full_text(msg))
        finally:
            self.disconnect(server)
        return msg

    def download_message_num(self, msg_num, *, decode=False, prompt=None):
        """
        обертка к методу download_message: получеает порядковый
        номер сообщения и конвертирует его в uid, затем - вызывает
        непосредственно download_message, с полученым uid;

        номер сообщения может быть целым числом.

        :param msg_num:
        :param decode:
        :param prompt:
        :return msg:
        """
        if not prompt:
            prompt = "num={}".format(int(msg_num))
        server = self.connect()
        num_to_uid = self.nums_to_uids(server)
        if not isinstance(msg_num, bytes):
            msg_num = str(msg_num).encode()  # Обязательно bytes!
        msg = self.download_message(num_to_uid[msg_num],
                                    server=server,
                                    decode=decode,
                                    prompt=prompt)
        return msg

    def __downloader(self, *, fetch_command, unseen_only, progress, loadfrom, decode, loaded_all,
                     initial_prompt=None, final_prompt=None, on_skip_text=None):
        """
        используется для загрузки сообщений или заголовков, в зависимости
        от параметра fetch_command;

        параметр unseen_only отвечает за загрузку всех итемов/только новых;

        progress - это функция, которая вызывается
        с параметрами (счетчик, всего);

        возвращает: [текст заголовков], [размеры сообщений],
        флаг "сообщения загружены полностью"
        проверка параметра mailconfig.fetch_limit для поддержки
        почтовых ящиков с большим количеством входящих сообщений: если он
        не равен None, извлекается только указанное число заголовков, вместо
        остальных возвращаются пустые заголовки;

        :param fetch_command:
        :param unseen_only:
        :param progress:
        :param loadfrom:
        :param decode:
        :param loaded_all:
        :param initial_prompt:
        :param final_prompt:
        :param on_skip_text:
        :return all_data, all_sizes, loaded_all:
        """
        server = self.connect()
        if initial_prompt:                  # сообшение о начале загрузки
            self.trace(initial_prompt)
        # все/новые?
        search_param = self.__search_all if not unseen_only else self.__search_all
        all_data = []       # тут будут все тектсы загруженных сообщений/заголовков
        all_sizes = []      # а здесь - размеры сообщений
        try:
            # получить строку, со всеми удовлетворяющими критериям поиска uid's
            status, response = server.uid("SEARCH", None, search_param)
            uids = response[0].split()            # каст строки в список
            if loadfrom > 1:                      # если надо грузить не с первого сообщения ->
                uids = uids[loadfrom - 1:]        # "урезать" список
            total = len(uids)                     # общее к-ство сообщений
            skip_to = total - self.fetch_limit    # крайний номер, который следует пропустить
            for (num, uid) in enumerate(uids, start=1):
                if progress: progress(num, total)
                if self.fetch_limit and (num <= skip_to):    # пропускаем
                    data = on_skip_text
                else:                                        # проводим загрузку
                    size_info = server.uid("FETCH", uid, "(UID RFC822.SIZE)")[1][0]   # инфо о размере сообщ.
                    all_sizes.append(int(size_info[size_info.rfind(b' ') + 1:-1]))    # из строки - числовое значение
                    data_info = server.uid("FETCH", uid, fetch_command)               # кортеж инфо о итеме
                    data = data_info[1][0][1]                                         # текст итема из кортежа
                if decode:      # если необходимо - декодируем
                    data = '\n'.join(self.decode_full_text(data))
                all_data.append(data)
        finally:
            self.disconnect(server)
        if final_prompt:                # сообщение о завершении загрузки
            self.trace(final_prompt)
        return all_data, all_sizes, loaded_all

    def download_all_headers(self, *, unseen_only=False, progress=None, loadfrom=1, decode=False):
        """
        получает только размеры и заголовки для всех или только
        для сообщений с номерами от loadfrom и выше;

        используйте loadfrom для загрузки только новых сообщений;

        для последующей загрузки полного текста
        сообщений используйте download_message;

        данный метод является оберткой над __downloader();

        :param unseen_only:
        :param progress:
        :param loadfrom:
        :param decode:
        :return:
        """
        return self.__downloader(
            fetch_command=self.__fetch_header,
            unseen_only=unseen_only,
            progress=progress,
            loadfrom=loadfrom,
            decode=decode,
            loaded_all=False,                                # сообщения загружены не полностью
            initial_prompt="Loading headers...",             # перед началом загрузки
            final_prompt="Loaded headers successful.",       # после загрузки
            on_skip_text=b"Subject: --Mail skipped--\n\n"    # для пропущеных - только заголовок с темой
        )

    def download_all_messages(self, *, unseen_only=False, progress=None, loadfrom=1, decode=False):
        """
        загрузить все сообщения целиком с номерами loadfrom...N,
        независимо от кэширования, которое может выполняться вызывающей
        программой;

        намного медленнее, чем downloadAllHeaders,
        если требуется загрузить только заголовки;

        поддержка mailconfig.fetch_limit: смотрите download_all_headers;

        данный метод является оберткой над __downloader();

        :param unseen_only:
        :param progress:
        :param loadfrom:
        :param decode:
        :return:
        """
        return self.__downloader(
            fetch_command=self.__fetch_header,
            unseen_only=unseen_only,
            progress=progress,
            loadfrom=loadfrom,
            decode=decode,
            loaded_all=True,                                                # сообщения загружены полностью
            initial_prompt="Loading messages...",
            final_prompt="Loaded messages successful.",
            on_skip_text=b"Subject: --Mail skipped--\n\nMail skipped.\n"    # для пропущеных - только заголовок + тема
        )

    def delete_messages(self, msgs_uid, *, progress=None, server=None):
        """
        удаляет сообщения c выбранными uid на сервере;

        :param msgs_uid:
        :param progress:
        :param server:
        """
        self.trace("Deleting messages...")
        if not server:
            server = self.connect()
        try:
            for ix, uid in enumerate(msgs_uid, start=1):
                if progress: progress(ix, len(msgs_uid))
                server.uid("STORE", uid, "+FLAGS", r"(\Deleted)")    # отметить флагом <\Deleted>
            server.expunge()                                         # удалить отмеченные
        finally:
            self.disconnect(server)

    def delete_messages_num(self, msgs_num, *, progress=None):
        """
        тот же функционал, что и delete_messages(), однако вместо
        uid - получает порядковые номера сообщений;

        полученый список конверитрует в соотвествующие uid,
        которые передает вышеозвученному методу;

        элементами списка могут быть номера сообщений типа int;

        :param msgs_num:
        :param progress:
        :return:
        """
        server = self.connect()
        nums_to_uids = self.nums_to_uids(server)
        if any(map(lambda x: isinstance(x, int), msgs_num)):
            msgs_num = map(lambda x: b'%d' % x if isinstance(x, int) else x, msgs_num)
        self.delete_messages([nums_to_uids[num] for num in msgs_num],   # конвертировать num -> uid
                             server=server, progress=progress)

    def get_password(self):
        """
        получает пароль для пользователя на указаном сервере,
        если он еще не известен, иначе - возвращает его;

        :return password:
        """
        if self.__password:             # если пароль известен -> вернуть его вызывающему
            return self.__password
        try:
            # попробовать прочитать пароль из файла, если таковой имеется
            with open(mailconfig.imap_password_file) as pswd_file:
                self.__password = pswd_file.readline()[:-1]
                self.trace("Password from local file {}".format(mailconfig.imap_password_file))
        except (FileNotFoundError, TypeError):
            # запросить пароль у пользователя
            return self.ask_password()

    def ask_password(self):       # этот метод нужно переопределить
        """
        абстрактный метод;

        реализация зависит от сферы использования подкласса,
        переопределяющего метод: консоль, GUI, Web, прочее;

        вне зависимости от реализации, метод должен возвращать
        полученный у пользователя пароль;

        :return password:
        """
        raise NotImplementedError("Subclass must define this method!")


# Специализированые подклассы
class MailFetcherConsole(MailFetcher):      # Для консоли
    def ask_password(self):
        import getpass
        prompt = "Password for {} on {}? ".format(self.user, self.host)
        return getpass.getpass(prompt)


class SilentMailFetcher(SilentMailTool, MailFetcher):       # Отключает трассировку
    def ask_password(self):
        pass
