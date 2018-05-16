from typing import NamedTuple

from envparse import env
from aiohttp import web


class RedisConfiguration(NamedTuple):
    host: str
    port: int
    minsize: int
    maxsize: int

    @classmethod
    def from_env(cls) -> 'RedisConfiguration':
        return cls(
            host=env.str('REDIS_HOST', default='localhost'),
            port=env.int('REDIS_PORT', default=6379),
            minsize=env.int('REDIS_POOL_MINSIZE', default=5),
            maxsize=env.int('REDIS_POOL_MAXSIZE', default=10),
        )


class Configuration(NamedTuple):
    redis: RedisConfiguration
    url_root: str

    @classmethod
    def from_env(cls) -> 'Configuration':
        return cls(
            redis=RedisConfiguration.from_env(),
            url_root=env.str('URL_ROOT', default='localhost:8080'),
        )


def setup_config(app: web.Application):
    app['config'] = Configuration.from_env()
