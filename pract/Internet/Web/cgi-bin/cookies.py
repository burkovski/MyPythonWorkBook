"""
создает или использует имя пользователя, сохраненное в cookies на стороне
клиента; в этом примере отсутствуют данные, получаемые из формы ввода
"""

import http.cookies
import os


cook_str = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cook_str)
user_cook = cookies.get("user")         # Извелчь, если был отправлен

if user_cook is None:                           # Создать при первом посещении
    cookies = http.cookies.SimpleCookie()       # Вывести заголовок Set-cookie
    cookies["user"] = "WebBeast"
    print(cookies)
    greeting = "<p>His name shall be... {}.</p>".format(cookies["user"])
else:
    greeting = "<p>Welcome back, {}!</p>".format(user_cook.value)

print("Content-type: text/html\n")
print(greeting)
