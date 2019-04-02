import aiohttp
import asyncio


URL = "https://www.python.org/"


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL)
        print(html)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
