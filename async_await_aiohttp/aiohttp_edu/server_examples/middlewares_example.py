from aiohttp import web


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as exc:
        if exc.status != 404:
            raise
        message = exc.reason
    return web.json_response({'error': message})


app = web.Application(middlewares=[error_middleware])
...
web.run_app(app)
