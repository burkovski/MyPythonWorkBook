from aiohttp import web


# create some handlers

async def handler(request):
    ...
    # do something with request
    ...
    return web.Response(text="Hello, world!")


async def post_handler(request):
    ...
    # do something with request
    ...
    return web.Response()


async def put_handler(request):
    ...
    # do something with request
    ...
    return web.Response()


async def all_handler(request):
    ...
    # do something with request
    ...
    return web.Response(text="Wildcard HTTP method")


# create an app
app = web.Application()
# register handlers
app.add_routes([
    web.route('*', '/wildcard', all_handler),       #
    web.get('/', handler),
    web.post('/post', post_handler),
    web.put('/put', put_handler)
])
web.run_app(app)
