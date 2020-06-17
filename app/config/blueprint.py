from app.resources.stock_resource import bp as stock_blueprint


class ConfigBluePrint:

    def config(self, app):
        app.register_blueprint(stock_blueprint)
