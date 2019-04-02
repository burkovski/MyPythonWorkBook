from aiohttp import web


async def hello(request):       # request handler - coroutine
    return web.Response(text="Hello, world")


# create an Application
app = web.Application()
# register the request handler on a
# particular HTTP method and path
app.add_routes([
    web.get('/', hello)
])
# run the application
web.run_app(app)
