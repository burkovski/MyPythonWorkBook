from aiohttp import web


routes = web.RouteTableDef()


@routes.view('/view')
class MyView(web.View):
    async def get(self):
        return web.Response(text="GET method to view")

    async def post(self):
        return web.Response(text="POST method to view")


app = web.Application()
app.router.add_routes(routes)
# or like that \/
# app.router.add_routes([
#     web.view('/view', MyView)
# ])
web.run_app(app)
