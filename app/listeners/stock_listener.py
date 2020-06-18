import logging

from app.config.app_context import ApplicationContext
from app.services.stock_service import analyze
from app.clients.heroku_client import health


class StockListener:

    def __init__(self, app_context):
        self.scheduler = app_context.scheduler

    def schedule(self):
        self.scheduler.schedule_job(
            self.__listen, interval=60)
        logging.info('Listening local Queue ')

    def __listen(self):
        app = ApplicationContext.instance()
        event = app.queue.get()

        analyze(event)

        health()
