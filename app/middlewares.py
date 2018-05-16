from typing import Dict

from aiohttp import web

from app.views import View, handle_404, handle_500


def create_error_middleware(overrides: Dict[int, View]):
    @web.middleware
    async def error_middleware(request: web.Request,
                               handler: View) -> web.Response:
        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override is not None:
                return await override(request)

            return response

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override is not None:
                return await override(request)

            raise

    return error_middleware


def setup_middlewares(app: web.Application):
    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
