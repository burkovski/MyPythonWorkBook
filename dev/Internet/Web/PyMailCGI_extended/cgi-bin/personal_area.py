import html_layout
import cgi


form = cgi.FieldStorage()

response = html_layout.HTMLMaker({key: form.getvalue(key) for key in form})
response.print_options_fields()
