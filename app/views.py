from typing import Callable, Awaitable, Union, Any, Dict
from urllib.parse import urljoin

from aiohttp import web
import aioredis
import aiohttp_jinja2
from marshmallow.exceptions import ValidationError

from app.schema import IndexSchema
from app.utils import shorten_url


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
    try:
        parsed, _ = IndexSchema().load(data)

    except ValidationError as err:
        return {
            "errors": err.messages['url'],
            "posted_url": data.get('url', "")
        }

    else:
        url = parsed['url']
        shortened = shorten_url(url)
        redis: aioredis.Redis = request.app['redis']
        await redis.set(shortened, url)
        return {
            'shortened': urljoin(f'http://{request.app["config"].url_root}', shortened),
            'index': request.app.router['index'].url_for(),
        }


def setup_routes(app: web.Application):
    app.router.add_routes(routes)
