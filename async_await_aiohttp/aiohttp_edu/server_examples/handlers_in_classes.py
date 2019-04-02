from aiohttp import web


class Handler:                  # handlers in Python-class
    def __init__(self):
        pass

    async def handle_intro(self, request):
        return web.Response(text="Hello, world")

    async def handle_greeting(self, request):
        name = request.match_info.get("name", "Anonymous")
        resp = "Hello, {}".format(name)
        return web.Response(text=resp)


handler = Handler()
app = web.Application()
app.router.add_routes([
    web.get("/intro", handler.handle_intro),
    web.get("/greet", handler.handle_greeting),
    web.get("/greet/{name}", handler.handle_greeting)
])
web.run_app(app)
