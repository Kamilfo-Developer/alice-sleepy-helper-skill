from aiohttp import web
from handlers import dp
from config import WEBHOOK_URL_PATH
from aioalice import get_new_configured_app


if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app)
