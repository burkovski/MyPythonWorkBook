import aiohttp_jinja2
import jinja2

from aiohttp import web


def validate_login(form):
    # do something with form (verify user)
    login = form.get('login')
    passwd = form.get('password')
    error = None if login and passwd else "Invalid login or password"
    return error


@aiohttp_jinja2.template('login_page.html')
async def login(request):
    if request.method == "POST":
        form = await request.post()
        error = validate_login(form)
        if error:
            return {"error": error}
        else:
            location = request.app.router['index'].url_for()
            raise web.HTTPFound(location=location)          # redirect to route, named 'index'
    return {"error": "request method should be POST"}


async def index(request):
    return web.Response(text="Welcome to index page!")


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('.'))      # setup jinja2 environment
app.add_routes([
    web.get('/index', index, name="index"),
    web.get('/login', login, name="login"),
    web.post('/login', login, name="login")
])
web.run_app(app)
