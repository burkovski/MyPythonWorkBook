"""
Вызывается при отправке формы в окне редактирования: завершает составление
нового сообщения, ответа или пересылаемого сообщения;
"""

import commonhtml
import cgi
import mailtools
import os

from secret import decode


def save_attachments(form, save_dir, max_attach=3):
    partnames = []
    for i in range(1, max_attach + 1):
        fieldname = "attach{}".format(i)
        if fieldname in form and form[fieldname].filename:
            fileinfo = form[fieldname]
            filedata = fileinfo.value
            filename = fileinfo.filename
            basename = os.path.basename(filename)
            partname = os.path.join(save_dir, basename)
            mode = 'rb' if isinstance(filedata, str) else 'wb'
            with open(partname, mode) as savefile:
                savefile.write(filedata)
            # os.chmod(partname, 766)
            partnames.append(partname)
    return partnames


save_dir = "parts_upload"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)


form = cgi.FieldStorage()
attaches = save_attachments(form, save_dir)
user, password, host = commonhtml.get_standard_smtp_fields(form)

from_hdr    = commonhtml.get_field(form, "From")
to_hdr      = commonhtml.get_field(form, "To")
cc_hdr      = commonhtml.get_field(form, "Cc")
subject_hdr = commonhtml.get_field(form, "Subject")
msg_text    = commonhtml.get_field(form, "Text")

parser = mailtools.MailParser()
to_hdr = parser.split_addresses(to_hdr)
cc_hdr = (parser.split_addresses(cc_hdr)
          if (cc_hdr and cc_hdr != '?')
          else '')
extra_hdrs = [("Cc", cc_hdr), ("X-Mailer", "PyMailCGI")]

try:
    body_enc = "ascii"
    msg_text.encode(body_enc)
except (UnicodeError, LookupError):
    body_enc = "utf-8"
attaches_enc = ["utf-8" for _ in range(len(attaches))]

sender = mailtools.SilentMailSenderAuth(host)
sender.user = user
sender.password = decode(password)
try:
    sender.send_message(
        from_hdr=from_hdr,
        to_list=to_hdr,
        subj_hdr=subject_hdr,
        extra_headers=extra_hdrs,
        body_text=msg_text,
        attaches=attaches,
        body_text_encoding=body_enc,
        attaches_encoding=attaches_enc
    )
except Exception as exc:
    commonhtml.error_page("Send mail error")
else:
    commonhtml.confirm_page("Send mail")
