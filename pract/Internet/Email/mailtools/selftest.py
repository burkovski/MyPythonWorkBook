import sys
import email.header

from mailtools import mailconfig
from mailtools import MailFetcherConsole, MailSenderAuthConsole, MailParser


sys.path.append("..")
print("Config from: {}".format(mailconfig.__file__))

sender = MailSenderAuthConsole(trace_size=5000)
sender.send_message(
    from_=mailconfig.my_address,
    to=["burkovski.danil@icloud.com", "burkovski.danil@gamil.com"],
    subj="Test mailtools package",
    extra_headers=[("X-Mailer", "Mailtools")],
    body_text="Here is my source code!\n",
    attaches=["selftest.py"],
    body_text_encoding="utf-8",
    attaches_encoding=["utf-8"],
)


def progress(now, total):
    print("{0:>3} form {1:<3}: {2:>3}%\r".format(now, total, int(now / total * 100)), end='')
    if now == total: print()


fetcher = MailFetcherConsole()
headers, sizes, loaded_all = fetcher.download_all_headers(progress=progress)
for num, hdr in enumerate(headers, start=1):
    print(hdr)
    if input("Load all message").strip() in {'y', 'Y'}:
        print(fetcher.download_message_num(b'%d' % num).rstrip(), '\n', '-'*70)

last5 = len(headers) - 4
print(len(headers), last5)
messages, sizes, loaded_all = fetcher.download_all_messages(progress=progress)
# for msg in messages:
#     print(msg[:200], '\n', '-'*70)

parser = MailParser()
print(len(messages))
for msg in messages:
    msg = parser.parse_message(msg)
    cont_type, main_text = parser.find_main_text(msg)
    raw_header, encoding = email.header.decode_header(msg["Subject"])[0]
    if encoding is None: continue
    try:
        header = raw_header.decode(encoding)
    except:
        encoding = msg["Content-type"].split()[-1].split('=')[-1]
        header = raw_header.decode(encoding)
    print("=" * 80)
    print("Parsed: {}".format(header))
    print(main_text)
input("Press <Enter> to exit")
