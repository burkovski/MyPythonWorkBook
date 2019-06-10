from aiohttp import web
from yarl import URL


routes = web.RouteTableDef()


@routes.get("/root", name="root")       # named route
async def handler(request):
    ...
    # build URL for resource named 'root'
    url = request.app.router["root"].url_for().with_query({'a': 'b', 'c': 'd'})
    assert url == URL("/root?a=b&c=d")
    ...
    url = request.app.router["user-info"].url_for(user="john_doe")
    url_with_qs = url.with_query("a=b")
    assert url_with_qs.human_repr() == "/john_doe/info?a=b"
    ...
    return web.Response(text="URL's are correct!")


app = web.Application()
...
# building URL for variable resources
app.router.add_resource(r'/{user}/info', name="user-info")
...
app.add_routes(routes)
web.run_app(app)



