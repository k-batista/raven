from app.resources.stock_resource import bp as stock_blueprint
from app.resources.bot_resource import bp as bot_blueprint


class ConfigBluePrint:

    def config(self, app):
        app.register_blueprint(stock_blueprint)
        app.register_blueprint(bot_blueprint)
