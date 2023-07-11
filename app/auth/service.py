from app.config import database
from .repository.repository import AuthRepository

class Service:
    def __init__(self):
        self.repository = AuthRepository(database)


def get_service():
    svc = Service()
    return svc
