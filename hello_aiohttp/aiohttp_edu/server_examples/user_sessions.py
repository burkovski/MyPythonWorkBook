import base64

from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage


async def handler(request):
    session = await get_session(request)
    last_visit = session.get("last_visit", None)
    text = "Last visited: {}".format(last_visit)
    return web.Response(text=text)


async def make_app():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    app.add_routes([web.get('/info', handler)])
    return app


web.run_app(make_app())
