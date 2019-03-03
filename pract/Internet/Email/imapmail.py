import imaplib
import getpass
import email.message
import pprint
from mailtools import mailconfig


def trace(*args):
    pprint.pprint(args)
    print("-" * 118)


mail_server = mailconfig.imap_servername
mail_user = mailconfig.imap_username
mail_password = getpass.getpass("Password for {}?".format(mail_server))


print("Connecting...")
server = imaplib.IMAP4_SSL(mail_server)
server.login(mail_user, mail_password)

try:
    trace(server.list())
    trace(server.select("INBOX"))
    trace(server.search(None, "ALL"))
    status, data = server.fetch(b'1', '(BODY.PEEK[HEADER] FLAGS)')
    msg = email.message_from_bytes(data[0][1], _class=email.message.Message)
    for key in msg.keys():
        hdr = email.header.decode_header(msg[key])[0][0]
        if isinstance(hdr, bytes): hdr = hdr.decode()
        trace('key: [{}]'.format(key), hdr)
    # trace(msg["From"])
    # trace(msg["To"])
    # trace(msg["Date"])
    # trace(msg["X-Mailing-List"])
    trace(email.header.decode_header(msg["Subject"])[0][0].decode("utf-8"))
    if msg.is_multipart():
        msg = msg.get_payload()[0]
    pprint.pprint(msg.get_payload(decode=True).decode())
finally:
    server.logout()
    # server.close()
