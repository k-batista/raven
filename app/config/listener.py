from app.listeners.stock_listener import StockListener


class ConfigListener:

    def config(self, app_context):
        StockListener(app_context).schedule()

        app_context.scheduler.start_listeners()
