"""
############################################################################
когда этот файл запускается как самостоятельный сценарий, выполняет
тестирование пакета
############################################################################
"""

#
# обычно используется модуль mailconfig, находящийся в каталоге клиента
# или в пути sys.path; для нужд тестирования берется модуль
# из каталога Email уровнем выше
#

from mailtools import mailconfig
import sys

sys.path.append('..')
print("file: {}".format(mailconfig.__file__))

# Получить из __init__
from pop_mailtools import MailFetcherConsole, MailSenderAuthConsole, MailParser


sender = MailSenderAuthConsole(trace_size=5000)
sender.send_message(From=mailconfig.my_address,
                    To=[mailconfig.my_address],
                    Subj="testing pop_mailtools package",
                    extra_hgrs=[("X-Mailer", "pop_mailtools")],
                    body_text="Here is my source code\n",
                    attaches=["selftest.py"])
                    # body_text_enc="utf-8",
                    # attaches_enc=["latin-1"],
                    # attaches=["monkeys.jpg"])


fetcher = MailFetcherConsole()


def status(*args):
    print(args)


hdrs, sizes, loaded_all = fetcher.download_all_headers(status)
for num, hdr in enumerate(hdrs):
    print(hdr)
    if input("Load mail?") in {'y', 'Y'}:
        print(fetcher.download_message(num+1).rstrip())
        print("-" * 70)


last5 = len(hdrs) - 4
msgs, sizes, loaded_all = fetcher.download_all_messages(status)
for msg in msgs:
    print(msg[:200])
    print("=" * 70)


parser = MailParser()
for msg in msgs:
    message = parser.parse_message(msg)
    cont_type, main_text = parser.find_main_text(message)
    print("Parsed: {}".format(message["Subject"]))
    print(main_text)
input("Press <Enter> to exit")

