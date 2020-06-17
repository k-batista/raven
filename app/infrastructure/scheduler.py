import atexit

from apscheduler.schedulers.background import BackgroundScheduler


class JobScheduler:
    def __init__(self, app):
        self.scheduler = BackgroundScheduler()

    def schedule_job(self, function, interval):
        self.scheduler.add_job(function, trigger="interval", seconds=interval)

    def schedule_job_son(self, function, data):
        self.scheduler.add_job(function, trigger='date', kwargs=data)

    def start_listeners(self):
        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown())
