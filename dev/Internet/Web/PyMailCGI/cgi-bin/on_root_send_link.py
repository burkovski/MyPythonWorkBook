"""
Вызывается щелчком на ссылке 'send' в главной странице: отображает страницу
составления нового сообщения
"""


import commonhtml
from mailtools import mailconfig


commonhtml.edit_page(
    kind="Write",
    headers={"From": mailconfig.smtp_user}
)
