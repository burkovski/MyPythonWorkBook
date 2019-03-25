import cgi
import commonhtml
import mailtools
import mailtools.mailconfig as mailconfig

from secret import decode


def quote_text(form):
    parser = mailtools.MailParser()
    address_headers = {"From", "To", "Cc", "Bcc"}
    quoted = "\n-----Original Message-----\n"
    for hdr in {"From", "To", "Date", "Subject"}:
        raw_hdr = commonhtml.get_field(form, hdr)
        parser_type = (parser.decode_address_header
                       if hdr in address_headers
                       else parser.decode_header)
        decoded = parser_type(raw_hdr)
        quoted += "{}: {}\n".format(hdr, decoded)
    quoted += '\n' + commonhtml.get_field(form, "Text")
    quoted = '\n' + quoted.replace('\n', '\n> ')
    return quoted


form = cgi.FieldStorage()
user, password, host = commonhtml.get_standard_smtp_fields(form)

try:
    if form["action"].value == "Reply":
        headers = {
            "From": mailconfig.my_address,
            "To": commonhtml.get_field(form, "From"),
            "Cc": mailconfig.my_address,
            "Subject": "Re: " + commonhtml.get_field(form, "Subject")
        }
        action = commonhtml.edit_page
        args = ("Reply", password, headers, quote_text(form))
    elif form["action"].value == "Forward":
        headers = {
            "From": mailconfig.my_address,
            "To": '',
            "Cc": mailconfig.my_address,
            "Subject": "Fwd: " + commonhtml.get_field(form, "Subject")
        }
        action = commonhtml.edit_page
        args = ("Forward", password, headers, quote_text(form))
    elif form["action"].value == "Delete":
        msg_num = form['msg_num'].value
        password = password
        fetcher = mailtools.SilentMailFetcher(host)
        fetcher.user = user
        fetcher.password = decode(password)
        fetcher.delete_messages_num([msg_num])
        action = commonhtml.confirm_page
        args = ("Delete", )
    else:
        raise ValueError("Invalid view action request")
except Exception:
    commonhtml.error_page("Cannot process view action")
else:
    action(*args)

