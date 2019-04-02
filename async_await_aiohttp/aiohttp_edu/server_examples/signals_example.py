from aiohttp import web
from aiopg.sa import create_engine


async def on_prepare(request, response):
    response.headers["My-Custom-Header"] = "MyValue"


async def create_aiopg(app):
    app["pg_engine"] = await create_engine(
        user="postgres_user",
        database="postgres_db",
        host="postgres_host",
        port=5432,
        password="postgres_password"
    )


async def dispose_aiopg(app):
    app["pg_engine"].close()
    await app["pg_engine"].wait_closed()


app = web.Application()
app.on_startup.append(create_aiopg)
app.on_response_prepare.append(on_prepare)
app.on_cleanup.append(dispose_aiopg)
web.run_app(app)
