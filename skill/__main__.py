from aioalice import get_new_configured_app
from aiohttp import web

from skill.config import WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL_PATH
from skill.handlers import dp

if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=int(WEBAPP_PORT), loop=dp.loop)
