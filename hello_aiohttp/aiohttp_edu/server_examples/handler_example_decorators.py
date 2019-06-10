from aiohttp import web


routes = web.RouteTableDef()


# create some handlers
@routes.get('/')
async def handler(request):
    ...
    # do something with request
    ...
    return web.Response(text="get handler")


@routes.post('/post')
async def post_handler(request):
    ...
    # do something with request
    ...
    return web.Response(text="post handler")


@routes.put('/put')
async def put_handler(request):
    ...
    # do something with request
    ...
    return web.Response(text="put handler")


@routes.route('*', '/wildcard')
async def all_handler(request):
    ...
    # do something with request
    ...
    return web.Response(text="Wildcard HTTP method")


# create an app
app = web.Application()
# register handlers
app.add_routes(routes)
web.run_app(app)
