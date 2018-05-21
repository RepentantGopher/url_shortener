from typing import Callable, Awaitable, Union, Any, Dict
import hashlib
from urllib.parse import urljoin

from aiohttp import web
import aioredis
import aiohttp_jinja2


Response = Awaitable[web.Response]
View = Callable[[web.Request], Response]

routes = web.RouteTableDef()


@aiohttp_jinja2.template('404.html', status=404)
async def handle_404(request: web.Request) -> Dict[str, Any]:
    return {
        'missing_path': request.path[1:],
    }


@aiohttp_jinja2.template('500.html', status=500)
async def handle_500(request: web.Request) -> Dict[str, Any]:
    return {}


@routes.get('/{shortened:[0-9a-zA-Z]{8}}')
async def get_url(request: web.Request) -> Union[Response, web.HTTPFound]:
    shortened = request.match_info['shortened']
    redis: aioredis.Redis = request.app['redis']
    url = await redis.get(shortened)
    if url is not None and len(url) > 0:
        return web.HTTPFound(url.decode())

    else:
        return await handle_404(request)


@routes.get('/', name="index")
@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Any:
    return {}


@routes.post('/')
@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Dict[str, Any]:
    data = await request.post()
    url = data['url']
    hash_object = hashlib.md5(url.encode())
    shortened = hash_object.hexdigest()[:8]
    redis: aioredis.Redis = request.app['redis']
    await redis.set(shortened, url)
    return {
        'shortened': urljoin(f'http://{request.app["config"].url_root}', shortened),
        'index': request.app.router['index'].url_for(),
    }


def setup_routes(app: web.Application):
    app.router.add_routes(routes)
