from aiohttp import web
from aiopg.sa import create_engine


async def pg_engine(app):
    app["pg_engine"] = await create_engine(
        user="postgres_user",
        database="postgres_db",
        host="postgres_host",
        port=5432,
        password="postgres_password"
    )
    yield
    app["pg_engine"].close()
    await app["pg_engine"].wait_closed()


app = web.Application()
app.cleanup_ctx.append(pg_engine)
...
web.run_app(app)
