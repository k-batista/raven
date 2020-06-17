import logging

from app.config.app_context import ApplicationContext
from app.services.stock_service import populate_database


class StockListener:

    def __init__(self, app_context):
        self.scheduler = app_context.scheduler

    def schedule(self):
        self.scheduler.schedule_job(
            self.__listen, interval=5)
        logging.info('Listening local Queue ')

    def __listen(self):
        app = ApplicationContext.instance()
        event = app.queue.get()

        populate_database(event)
