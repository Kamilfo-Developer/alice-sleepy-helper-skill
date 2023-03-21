from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL_PATH = os.getenv("WEBHOOK_URL_PATH")

WEBAPP_HOST = os.getenv("WEBAPP_HOST")

WEBAPP_PORT = os.getenv("WEBAPP_PORT")
