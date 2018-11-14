"""
############################################################################
получает, удаляет, сопоставляет почту с POP-сервера (описание и тест
приводятся в модуле __init__)
############################################################################
"""

import mailconfig
import poplib
import sys
print("User: {}".format(mailconfig.pop_username))

from .mailparser import MailParser                      # Сопоставление заголовков
from .mailtool import MailTool, SilentMailTool          # Суперкласс упр. трассировкой

# Рассинхронизация номеров сообщений
class DeleteSyncError(Exception):           # обнаружена рассинхр-я при удалении
    pass

class TopNotSupported(Exception):           # невозможно выполнить проверку синхронизации
    pass

class MessageSyncError(Exception):          # обнаружена рассинхр-я оглавления
    pass


class MailFetcher(MailTool):
    """
    получение почты: соединяется, извлекает заголовки+содержимое, удаляет
    работает на любых компьютерах с Python+Интернет; создайте подкласс,
    чтобы реализовать кэширование средствами протокола POP;
    для поддержки протокола IMAP требуется создать новый класс;
    предусматривает декодирование полного текста сообщений
    для последующей передачи его механизму анализа;
    """
    def __init__(self, pop_server=None, pop_user=None, pop_password=None, hastop=True):
        self.pop_server = pop_server or mailconfig.pop_servername
        self.pop_user = pop_user or mailconfig.pop_username
        self.serv_hastop = hastop
        self.pop_password = pop_password    # Если имеет значение None, пароль будет запрошен позднее

    def connect(self):
        self.trace("Connecting...")
        self.get_password()                 # Файл, GUI или консоль
        try:
            server = poplib.POP3(self.pop_server)
        except poplib.error_proto:
            server = poplib.POP3_SSL(self.pop_server)
        server.user(self.pop_user)          # Соединиться, зарегистрироваться
        server.pass_(self.pop_password)
        self.trace(server.getwelcome())
        return server

    # использовать настройки из клиентского mailconfig, находящегося в пути
    # поиска; при необходимости можно изменить в классе или в экземплярах;
    fetch_encoding = mailconfig.fetch_encoding

    def decode_full_text(self, msg_bytes):
        """
        декодирует полный текст сообщения, представленный в виде
        строки bytes, в строку Юникода str; выполняется на этапе получения
        для последующего отображения или анализа (после этого полный текст
        почтового сообщения всегда будет обрабатываться как строка Юникода);
        декодирование выполняется в соответствии с настройками в классе или
        в экземпляре или применяются наиболее распространенные кодировки;
        можно было бы также попробовать определить кодировку из заголовков
        или угадать ее, проанализировав структуру байтов; в Python 3.2/3.3
        этот этап может оказаться излишним: в этом случае измените метод
        так, чтобы он возвращал исходный список строк сообщения нетронутым;
        дополнительные подробности смотрите в главе 13;
        для большинства сообщений достаточно будет простой 8-битовой
        кодировки, такой как latin-1, потому что стандартной считается
        кодировка ASCII; этот метод применяется ко всему тексту сообщения -
        это лишь один из этапов на пути декодирования сообщений: содержимое
        и заголовки сообщений могут также находиться в формате MIME и быть
        закодированы в соответствии со стандартами электронной почты
        и Юникода; смотрите подробности в главе 13, а также реализацию
        модулей mailParser и mailSender;
        """
        text = None
        kinds = [self.fetch_encoding]
        kinds.extend(("ascii", "latin-1", "utf-8"))
        kinds.append(sys.getdefaultencoding())
        for kind in kinds:
            try:
                text = [line.decode(kind) for line in msg_bytes]
                break
            except (UnicodeError, LookupError):
                pass
        if text is None:
            blank_line = msg_bytes.index(b'')
            hdrs_only = msg_bytes[:blank_line]
            commons = ["ascii", "latin-1", "utf-8"]
            for common in commons:
                try:
                    text = [line.decode(common) for line in hdrs_only]
                    break
                except UnicodeError:
                    pass
            else:
                try:
                    text = [line.decode() for line in hdrs_only]
                except UnicodeError:
                    text = ["From: (sender of unknown Unicode format headers)"]
            text.extend(('', "-- Sorry: mailtools cannot decode this mail content!--"))
        return text

    def download_message(self, msg_num):
        """
        загружает полный текст одного сообщения по указанному относительному
        номеру POP msgnum; анализ содержимого выполняет вызывающая программа
        """
        self.trace("Load: {}".format(msg_num))
        server = self.connect()
        try:
            resp, msg_lines, resp_size = server.retr(msg_num)
        finally:
            server.quit()
        msg_lines = self.decode_full_text(msg_lines)
        return '\n'.join(msg_lines)         # объединить строки

    def download_all_headers(self, progress=None, loadfrom=1):
        """
        получает только размеры и заголовки для всех или только
        для сообщений с номерами от loadfrom и выше;
        используйте loadfrom для загрузки
        только новых сообщений; для последующей загрузки полного текста
        сообщений используйте download_message; progress - это функция,
        которая вызывается с параметрами (счетчик, всего);
        возвращает: [текст заголовков], [размеры сообщений],
        флаг "сообщения загружены полностью"
        добавлена проверка параметра mailconfig.fetch_limit для поддержки
        почтовых ящиков с большим количеством входящих сообщений: если он
        не равен None, извлекается только указанное число заголовков, вместо
        остальных возвращаются пустые заголовки; иначе пользователи,
        получающие большое количество сообщений, как я (4K сообщений),
        будут испытывать неудобства;
        передает loadfrom методу download_all_messages (чтобы хоть
        немного облегчить положение);
        """
        if not self.serv_hastop:        # Не все серверы поддерживают команду TOP
            # Загрузить полные сообщения
            return self.download_all_messages(progress, loadfrom)
        else:
            self.trace("Loading headers")
            fetch_limit = mailconfig.fetch_limit
            server = self.connect()                 # Ящик теперь заблокиррван до вызова метода quit
            try:
                resp, msgs_info, resp_sz = server.list()        # Список строк 'номер размер'
                msg_count = len(msgs_info)              # Альтернатива методу server.stat()[0]
                msgs_info = msgs_info[loadfrom-1:]      # Пропустить уже загруженные (если имеются)
                all_sizes = [int(x.split()[1]) for x in msgs_info]
                all_hdrs = []
                for msg_num in range(loadfrom, msg_count+1):
                    if progress:
                        progress(msg_num, msg_count)
                    if fetch_limit and (msg_num <= msg_count - fetch_limit):
                        # Пропустить, добавить пустой заголовок
                        hdr_text = "Subject: --mail skipped--\n\n"
                        all_hdrs.append(hdr_text)
                    else:
                        # Получить только заголовки
                        resp, hdr_lines, resr_sz = server.top(msg_num, 0)
                        hdr_lines = self.decode_full_text(hdr_lines)
                        all_hdrs.append(hdr_lines)
            finally:
                server.quit()
            assert len(all_hdrs) == len(all_sizes)
            self.trace("Load headers exit")
            return all_hdrs, all_sizes, False

    def download_all_messages(self, progress=None, loadfrom=1):
        """
        загрузить все сообщения целиком с номерами loadfrom..N,
        независимо от кэширования, которое может выполняться вызывающей
        программой; намного медленнее, чем downloadAllHeaders,
        если требуется загрузить только заголовки;
        поддержка mailconfig.fetch_limit: смотрите download_all_headers;
        можно было бы использовать server.list() для получения размеров
        пропущенных сообщений, но клиентам скорее всего этого не требуется;
        """
        self.trace("Loading full messages")
        fetch_limit = mailconfig.fetch_limit
        server = self.connect()
        try:
            msg_count, msg_bytes = server.stat()
            all_msgs = []
            all_sizes = []
            for msg_num in range(loadfrom, msg_count+1):          # Пусто, если low >= high
                if progress:
                    progress(msg_num, msg_count)
                if fetch_limit and (msg_num <= msg_count - fetch_limit):
                    # Пропустить, добавить пустое сообщение
                    mail_text = "Subject: --mail skipped--\n\nMail skipped.\n"
                    all_msgs.append(mail_text)
                else:
                    # Получить полные сообщения
                    resp, msg, resp_sz = server.retr(msg_num)
                    msg = self.decode_full_text(msg)
                    all_msgs.append('\n'.join(msg))
                    all_sizes.append(resp_sz)
        finally:
            server.quit()
        assert len(all_msgs) == msg_count - loadfrom + 1        # Нумерация, начиная с 1
        return all_msgs, all_sizes, True

    def delete_messages(self, msg_nums, progress=None):
        """
        удаляет несколько сообщений на сервере; предполагается, что номера
        сообщений в ящике не изменялись с момента последней
        синхронизации/загрузки; используется, если заголовки сообщения
        недоступны; выполняется быстро, но может быть опасен: смотрите
        delete_messages_safely
        """
        self.trace("Deleting mails")
        server = self.connect()
        try:
            for ix, msg_num in enumerate(msg_nums):
                if progress:
                    progress(ix+1, len(msg_nums))
                server.dele(msg_num)
        finally:
            server.quit()

    def delete_messages_safely(self, msg_nums, sync_hdrs, progress=None):
        """
        удаляет несколько сообщений на сервере, но перед удалением выполняет
        проверку заголовка с помощью команды TOP; предполагает, что почтовый
        сервер поддерживает команду TOP протокола POP, иначе возбуждает
        исключение TopNotSupported - клиент может вызвать deleteMessages;
        используется, если почтовый ящик на сервере мог измениться с момента
        последней операции получения оглавления и соответственно могли
        измениться номера POP-сообщений; это может произойти при удалении
        почты с помощью другого клиента; кроме того, некоторые провайдеры
        могут перемещать почту из ящика входящих сообщений в ящик
        недоставленных сообщений в случае ошибки во время загрузки;
        аргумент synchHeaders должен быть списком уже загруженных
        заголовков, соответствующих выбранным сообщениям
        (обязательная информация);
        возбуждает исключение, если обнаруживается рассинхронизация
        с почтовым сервером; доступ к входящей почте
        блокируется до вызова метода quit, поэтому номера не могут
        измениться между командой TOP и фактическим
        удалением: проверка синхронизации должна выполняться здесь,
        а не в вызывающей программе; может оказаться недостаточным
        вызвать checkSynchError+deleteMessages, но здесь проверяется
        каждое сообщение, на случай удаления или вставки
        сообщений в середину почтового ящика;
        """
        if not self.serv_hastop:
            raise TopNotSupported("Safe delete canceled!")
        self.trace("Deleting messages safely")
        err_msg = "Message {} out of sync with server.\n"
        err_msg += "Delete terminated at this message.\n"
        err_msg += "MAil client may required restart or reload."
        server = self.connect()
        try:
            msg_count, msg_bytes = server.stat()      # Объем входящей почты
            for ix, msg_num in enumerate(msg_nums):
                if progress:
                    progress(ix+1, len(msg_nums))
                if msg_num > msg_count:               # Сообщения были удалены?
                    raise DeleteSyncError(err_msg.format(msg_num))
                resp, hdr_lines, resp_sz = server.top(msg_num, 0)       # Только заголовок
                hdr_lines = self.decode_full_text(hdr_lines)
                msg_hdrs = '\n'.join(hdr_lines)
                if not self.headers_match(msg_hdrs, sync_hdrs[msg_num-1]):
                    raise DeleteSyncError(err_msg.format(msg_num))
                else:
                    server.dele(msg_num)
        finally:
            server.quit()

    def check_sync_error(self, sync_hdrs):
        """
        сопоставляет уже загруженные заголовки в списке synchHeaders с теми,
        что находятся на сервере, с использованием команды TOP
        протокола POP, извлекающей текст заголовков;
        используется, если содержимое почтового ящика могло измениться,
        например в результате удаления сообщений с помощью другого клиента
        или в результате автоматических действий, выполняемых
        почтовым сервером; возбуждает исключение в случае обнаружения
        рассинхронизации или ошибки во время взаимодействия с сервером;
        для повышения скорости проверяется только последний в последнем:
        это позволяет обнаружить факт удаления из ящика, но предполагает,
        что сервер не мог вставить новые сообщения перед последним (верно
        для входящих сообщений); сначала проверяется объем входящей почты:
        если меньше - были только удаления; иначе, если сообщения удалялись
        и в конец добавлялись новые, результат top будет отличаться;
        результат этого метода можно считать действительным только на момент
        его работы: содержимое ящика входящих сообщений может
        измениться после возврата;
        """
        self.trace("Sync check")
        err_msg = "Messages index out of with mail server.\n"
        err_msg += "Mail client may require restart or reload."
        server = self.connect()
        try:
            last_num = len(sync_hdrs)
            msg_count, msg_bytes = server.stat()        # Объем входящей почты
            if last_num > msg_count:                    # Теперь меньше?
                raise MessageSyncError(err_msg)
            if self.serv_hastop:
                resp, hdr_lines, resp_sz = server.top(last_num, 0)
                hdr_lines = self.decode_full_text(hdr_lines)
                last_msg_hdrs = '\n'.join(hdr_lines)
                if not self.headers_match(last_msg_hdrs, sync_hdrs[-1]):
                    raise MessageSyncError(err_msg)
        finally:
            server.quit()

    def headers_match(self, hdr_text1, hdr_text2):
        """
        для сопоставления недостаточно простого сравнения строк: некоторые
        серверы добавляют заголовок "Status:", который изменяется с течением
        времени; у одного провайдера он устанавливался изначально
        как "Status: U" (unread - непрочитанное) и заменялся на "Status: RO"
        (read, old - прочитано, старое) после загрузки сообщения -
        это сбивает с толку механизм проверки синхронизации,
        если после загрузки нового оглавления, но непосредственно
        перед удалением или проверкой последнего сообщения клиентом
        было загружено новое сообщение;
        теоретически значение заголовка "Message-id:" является уникальным
        для сообщения, но сам заголовок является необязательным и может
        быть подделан; сначала делается попытка выполнить более типичное
        сопоставление; анализ - дорогостоящая операция, поэтому
        выполняется последним
        """
        # Попробовать сравнить строки
        if hdr_text1 == hdr_text2:
            self.trace("Same headers text")
            return True

        # Попробовать сопоставить без заголовков Status
        split1 = hdr_text1.splitlines()
        split2 = hdr_text2.splitlines()
        strip1 = [line for line in split1 if not line.startswith("Status:")]
        strip2 = [line for line in split2 if not line.startswith("Status:")]
        if strip1 == strip2:
            self.trace("Same without Status")
            return True

        # Попробовать найти несовпадения заголовков message-id,
        # если они имеются
        msgid1 = [line for line in split1 if line[:11].lower() == "message-id:"]
        msgid2 = [line for line in split2 if line[:11].lower() == "message-id:"]
        if (msgid1 or msgid2) and (msgid1 != msgid2):
            self.trace("Different Message-ID")
            return False

        # Выполнить полный анализ заголовков и сравнить наиболее типичные
        # из них, если заголовки message-id отсутствуют или в них были найдены различия
        try_hdrs = ("From", "To", "Subject", "Date")
        try_hdrs += ("Cc", "Return-Path", "Received")
        msg1 = MailParser().parse_headers(hdr_text1)
        msg2 = MailParser().parse_headers(hdr_text2)
        for hdr in try_hdrs:        # Возможны несколько адресов в Received
            if msg1.get_all(hdr) != msg2.get_all(hdr):      # Без учета регистра
                self.trace("Different common headers")
                return False

        # Все обычные заголовки совпадают
        # и нет ращличащихся message-id
        self.trace("Same common headers")
        return True

    def get_password(self):
        """
        получает пароль POP, если он еще не известен
        не требуется до обращения к серверу из файла
        на стороне клиента или вызовом метода подкласса
        """
        if not self.pop_password:
            try:
                local_file = open(mailconfig.pop_passwd_file)
                self.pop_password = local_file.readline()[:-1]
                self.trace("Local file password {}".format(repr(self.pop_password)))
            except FileNotFoundError:
                self.pop_password = self.ask_pop_password()

    def ask_pop_password(self):
        assert False, "Subclass must define method"


# Специализированые подклассы
class MailFetcherConsole(MailFetcher):
    def ask_pop_password(self):
        import getpass
        prompt = "Password for {} on {}?".format(self.pop_user, self.pop_server)
        return getpass.getpass(prompt)


class SilentMailFetcher(SilentMailTool, MailFetcher):
    pass     # Отключает трассировку
