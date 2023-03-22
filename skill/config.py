from dotenv import load_dotenv
import os

load_dotenv()

WEBHOOK_URL_PATH = os.getenv("WEBHOOK_URL_PATH") or "/"

WEBAPP_HOST = os.getenv("WEBAPP_HOST") or "localhost"

WEBAPP_PORT = os.getenv("WEBAPP_PORT") or 5555
