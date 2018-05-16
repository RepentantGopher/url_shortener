from typing import Callable, Awaitable, Union, Any
import hashlib
from urllib.parse import urljoin

from aiohttp import web
import aioredis
import aiohttp_jinja2


Response = Awaitable[web.Response]
View = Callable[[web.Request], Response]

routes = web.RouteTableDef()


async def handle_404(request: web.Request) -> Response:
    return web.json_response(data={}, status=404)


async def handle_500(request: web.Request) -> Response:
    return web.json_response(data={}, status=500)


@routes.get('/{shortened:[0-9a-zA-Z]{8}}')
async def get_url(request: web.Request) -> Union[Response, web.HTTPFound]:
    shortened = request.match_info['shortened']
    redis: aioredis.Redis = request.app['redis']
    url = await redis.get(shortened)
    if url is not None:
        return web.HTTPFound(url.decode())

    else:
        return await handle_404(request)


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Any:
    return {}


@routes.post('/')
@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Any:
    data = await request.post()
    url = data['url']
    hash_object = hashlib.md5(url.encode())
    shortened = hash_object.hexdigest()[:8]
    redis: aioredis.Redis = request.app['redis']
    await redis.set(shortened, url)
    return {
        'shortened': urljoin(f'http://{request.app["config"].url_root}', shortened)
    }


def setup_routes(app: web.Application):
    app.router.add_routes(routes)
