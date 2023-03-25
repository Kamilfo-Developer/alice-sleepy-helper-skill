from skill.config import WEBHOOK_URL_PATH, WEBAPP_HOST, WEBAPP_PORT
from skill.handlers import dp
from aioalice import get_new_configured_app
from aiohttp import web

if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=int(WEBAPP_PORT), loop=dp.loop)
