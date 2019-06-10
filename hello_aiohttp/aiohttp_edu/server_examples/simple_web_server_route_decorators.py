from aiohttp import web

# create route table
routes = web.RouteTableDef()


@routes.get('/')            # register handler in routes with decorator
async def hello(request):
    return web.Response(text="Hello, world")


app = web.Application()
app.add_routes(routes)      # add routes to common route table
web.run_app(app)
