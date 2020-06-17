from queue import Queue

from app.infrastructure.scheduler import JobScheduler
from app.repositories.stock_repository import StockRepository


class ApplicationContext(object):
    __instance = None

    def __init__(self, app, db):
        self.scheduler = JobScheduler(app)
        self.queue = Queue()
        self.stock_repository = StockRepository(app, db)

        ApplicationContext.__instance = self

    @staticmethod
    def instance():
        return ApplicationContext.__instance
