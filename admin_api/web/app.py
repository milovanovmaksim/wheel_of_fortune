from typing import Optional

from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest,)
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as setup_aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage


from admin_api.store.store import setup_store, Store
from admin_api.web.config import Config, setup_config
from admin_api.web.logger import setup_logging
from admin_api.web.middlewares import setup_middlewares
from admin_api.web.routes import setup_routes
from store.database.database import Database
from store.admin.models import Admin


class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database: Optional[Database] = None


class Request(AiohttpRequest):
    admin: Optional[Admin] = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})

    @property
    def query(self) -> dict:
        return self.request.get("querystring")


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_aiohttp_session(app, EncryptedCookieStorage(cookie_name='sessionid',
                                                      secret_key=app.config.session.key))
    setup_aiohttp_apispec(app, static_path='/swagger_static',
                          title='vk-bot', url='/docs/json',
                          swagger_path='/docs')
    setup_routes(app)
    setup_middlewares(app)
    setup_store(app)
    return app
