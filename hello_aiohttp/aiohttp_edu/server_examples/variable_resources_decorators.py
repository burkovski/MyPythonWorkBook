from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/greeting/{name}")
async def greater(request):
    return web.Response(text="Hello, {}".format(request.match_info.get("name")))


app = web.Application()
app.add_routes(routes)
web.run_app(app)
