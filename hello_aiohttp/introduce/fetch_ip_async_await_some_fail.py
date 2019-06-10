import time
import asyncio
import aiohttp

from collections import namedtuple


Service = namedtuple("Service", ("name", "url", "ip_attr"))

SERVICES = (
    Service("ipify", "https://api.ipify.org?format=json", "ip"),
    Service("ip-api", "http://ip-api.com/json", "query"),
    Service("broken", "http://no-way-this-is-going-to-work.com/json", "ip")     # такого URL нет!
)


async def fetch_ip(session, service):
    start = time.time()
    print("Fetch IP from {}".format(service.name))
    try:
        async with session.get(service.url) as response:
            json_response = await response.json()
            ip = json_response[service.ip_attr]
    except aiohttp.ClientConnectionError:
        res = "{} is unresponsive".format(service.name)
    else:
        res = "{} finished with result: {}, took: {:.2f} seconds".format(
            service.name, ip, time.time() - start
        )
    return res


async def asynchronous():
    async with aiohttp.ClientSession() as session:
        futures = [fetch_ip(session, service)
                   for service in SERVICES]
        done, pending = await asyncio.wait(futures)
        for future in pending:      # завершить еще не заверщенные
            future.cancel()
        for future in done:
            print(future.result())  


loop = asyncio.get_event_loop()
loop.run_until_complete(asynchronous())
loop.close()
