import cgi

from config import *
from html_layout import HTMLMaker


options = {
    OptionsKeys.kind          : "Sign in!",
    FormFields.handler_script : "verify.py",
    FormFields.verify_mode    : FormFields.vm_sign_in,
    OptionsKeys.extra_fields  : None
}

form = cgi.FieldStorage()
options.update((key, form.getvalue(key)) for key in form)
layout = HTMLMaker(options)
layout.password_page()
