from aiohttp import web
import aiohttp_jinja2
import jinja2

from app.settings import setup_config
from app.redis import setup_redis
from app.middlewares import setup_middlewares
from app.views import setup_routes


app = web.Application()
setup_routes(app)
setup_config(app)
setup_redis(app)
setup_middlewares(app)
aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('app', 'templates'))


if __name__ == "__main__":
    web.run_app(app)
