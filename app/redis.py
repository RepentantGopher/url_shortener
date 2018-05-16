import aioredis
from aiohttp import web

from app.settings import RedisConfiguration


async def init_redis(app: web.Application):
    conf: RedisConfiguration = app['config'].redis
    app['redis'] = await aioredis.create_redis_pool(
        f'redis://{conf.host}:{conf.port}',
        minsize=conf.minsize,
        maxsize=conf.maxsize,
        loop=app.loop
    )


async def close_redis(app: web.Application):
    redis: aioredis.Redis = app['redis']
    redis.close()
    await redis.wait_closed()


def setup_redis(app: web.Application):
    app.on_startup.append(init_redis)
    app.on_cleanup.append(close_redis)
