from app.config import database
from .adapters.serviceST import Tarih
from .adapters.openai_service import OpenAI
from .repository.repository import History
from dotenv import load_dotenv

load_dotenv()

openai_key = os.environ["OPENAI_API_KEY"]
openai.api_key = openai_key


class Service:
    def __init__(self):
        self.tarih = Tarih()
        self.repository = History(database)
        self.openai = OpenAI(openai_key)

def get_service():
    svc = Service()
    return svc
