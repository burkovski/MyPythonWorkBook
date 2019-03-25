import cgi
import commonhtml
import loadmail
import mailtools.mailparser as mp

from secret import encode


max_headers = 35
form = cgi.FieldStorage()
user, password, host = commonhtml.get_standard_imap_fields(form)
parser = mp.MailParser()

try:
    new_messages = loadmail.load_mail_headers(host, user, password)
    messages_list = []
    address_headers = {"From", "To", "Cc", "Bcc"}
    keys = ("Subject", "From", "Date")
    max_len = max(len(key) for key in keys)
    for msg_num, msg in enumerate(new_messages, start=1):
        msg_info = []
        headers = parser.parse_headers(msg)
        for key in keys:
            raw_header = headers.get(key, '?')
            parser_type = (parser.decode_address_header
                           if key in address_headers
                           else parser.decode_header)
            decoded = parser_type(raw_header)
            # if key == "Date":
            #     decoded = ' '.join(decoded.split(' ')[:-2])
            msg_info.append("{}: {}".format(key.rjust(max_len), decoded))
        msg_info = '\n'.join(msg_info)
        messages_list.append((msg_info, commonhtml.url_root + "on_view_list_link.py",
                              {"msg_num" : msg_num,
                               "user"    : user,
                               "password": password,
                               "host"    : host}))
    commonhtml.list_page(reversed(messages_list))
except Exception:
    commonhtml.error_page("Error loading mail index")
