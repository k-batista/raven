import os 
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import MapperExtension


app = Flask(__name__)
url = os.getenv('DATABASE_URL')
if url:
    app.config['SQLALCHEMY_DATABASE_URI'] = url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://raven_adm:raven_adm@localhost:5405/db_raven'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class AuditExtension(MapperExtension):

    def before_insert(self, mapper, connection, instance):
        instance.dat_create = datetime.utcnow()
        instance.dat_update = datetime.utcnow()

    def before_update(self, mapper, connection, instance):
        instance.dat_create = instance.dat_create
        instance.dat_update = datetime.utcnow()

        
class Base(db.Model):
    __abstract__ = True
    __table_args__ = {'schema': 'raven'}

    __mapper_args__ = {'extension': AuditExtension()}

    dat_create = db.Column(db.DateTime, default=datetime.now, nullable=False)
    dat_update = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False)


class Stock(Base):
    __tablename__ = 'stock'

    id_stock = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    time_frame = db.Column(db.String, nullable=False)
    quote_date = db.Column(db.String, nullable=False)
    quote = db.Column(JSONB, nullable=False)
    indicators = db.Column(JSONB, nullable=False)


if __name__ == '__main__':
    manager.run()


# op.execute('create schema raven')