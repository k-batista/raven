# monkey_patch deve ser feito antes de tudo, depois o import e initialize do newrelic
# altera timezone para que o log informe o horario correto
# e so entao ocorre o start da aplicacao
import gevent.monkey; gevent.monkey.patch_all()

import time
import os
from flask import send_from_directory

from app.config.server import Server
from app.config.listener import ConfigListener
from app.infrastructure.database import db
from app.config.app_context import ApplicationContext


def create_server():
    # Configuracao server : Flask
    app = Server().config()

    __set_timezone()

    # Configuracao Banco de Dados: SQLAlchemy
    db.init_app(app)

    app_context = ApplicationContext(app, db)

    ConfigListener().config(app_context)

    return app


def __set_timezone():
    os.environ['TZ'] = 'America/Sao_Paulo'
    time.tzset()

#
# Create app
app = create_server()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)
