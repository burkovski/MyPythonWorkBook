import cgi

from config import *
from html_layout import HTMLMaker


options = {
    OptionsKeys.kind          : "Sign up!",
    FormFields.handler_script : "verify.py",
    FormFields.verify_mode    : FormFields.vm_sign_up,
    OptionsKeys.extra_fields  : {
        "caption": "Repeat password:",
        "field": '<input type="password" name="{0}">'.format(FormFields.repeat_password)
    }
}

form = cgi.FieldStorage()
options.update((key, form.getvalue(key)) for key in form)
layout = HTMLMaker(options)
layout.password_page()
