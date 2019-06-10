from aiohttp import web


class AcceptChooser:
    def __init__(self):
        self._accepts = {}

    async def do_route(self, request):
        for accept in request.headers.getall("ACCEPT", []):
            acceptor = self._accepts.get(accept)
            if acceptor is not None:
                return await acceptor(request)
        raise web.HTTPNotAcceptable()

    def reg_acceptor(self, accept, handler):
        self._accepts[accept] = handler


async def handle_json(request):
    # do json handling
    ...


async def handle_xml(request):
    # do xml handling
    ...


app = web.Application()
chooser = AcceptChooser()
app.add_routes([
    web.get('/', chooser.do_route)
])

chooser.reg_acceptor('application/json', handle_json)
chooser.reg_acceptor('application/xml', handle_xml)
web.run_app(app)
