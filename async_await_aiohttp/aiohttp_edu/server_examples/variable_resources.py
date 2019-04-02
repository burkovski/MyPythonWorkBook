from aiohttp import web


async def greater(request):
    # get name param from request instance
    return web.Response(
        text="Hello, {}".format(request.match_info.get("name", "Anonymous"))
    )


app = web.Application()
app.add_routes([
    web.get("/greeting", greater),
    web.get("/greeting/{name}", greater)        # name - variable
])
web.run_app(app)
