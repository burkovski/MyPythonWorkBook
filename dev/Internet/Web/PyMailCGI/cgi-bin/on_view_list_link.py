import cgi
import commonhtml
import secret
import os
import mailtools


def save_attachments(message, parser, save_dir="parts_download"):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    for filename in os.listdir(save_dir):
        path = os.path.join(save_dir, filename)
        os.remove(path)
    part_files = parser.save_parts(save_dir, message)
    filenames = [filename for (cont_type, filename) in part_files]
    for filename in filenames:
        os.chmod(filename, 765)
    return filenames


form = cgi.FieldStorage()
user, password, host = commonhtml.get_standard_imap_fields(form)
# password = secret.decode(password)

try:
    msg_num = form["msg_num"].value
    parser = mailtools.MailParser()
    fetcher = mailtools.SilentMailFetcher(host)
    fetcher.user = user
    fetcher.password = password
    full_text = fetcher.download_message_num(msg_num)
    msg_obj = parser.parse_message(full_text)
    parts = save_attachments(msg_obj, parser)
    cont_type, msg_text = parser.find_main_text(msg_obj)
except Exception:
    commonhtml.error_page("Error loading message " + password)
else:
    commonhtml.view_page(msg_num, msg_obj, msg_text, form, parts)
