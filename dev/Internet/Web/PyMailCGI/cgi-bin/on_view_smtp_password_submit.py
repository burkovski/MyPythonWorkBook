import cgi
import commonhtml
import mailtools.mailparser as mp

from secret import encode


max_headers = 35
form = cgi.FieldStorage()
user, password, host = commonhtml.get_standard_smtp_fields(form)
parser = mp.MailParser()


commonhtml.edit_page(
    kind="Write",
    password=encode(password),
    headers={"From": user}
)
