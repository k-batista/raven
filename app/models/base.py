from datetime import datetime

from dynaconf import settings
from sqlalchemy import func, types
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import MapperExtension


from app.infrastructure.database import db

db_crypt_key = settings.DB_CRYPT.KEY


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


class EncryptedColumn(types.TypeDecorator):
    impl = TEXT

    def bind_expression(self, bindvalue):
        encrypt_function = func.encrypt(
            bindvalue, db_crypt_key, settings.DB_CRYPT.ALGORITHM)
        return func.encode(
            encrypt_function,
            settings.DB_CRYPT.ENCODE_ALGORITHM)

    def column_expression(self, col_value):
        decode_base64_function = func.decode(
            col_value, settings.DB_CRYPT.ENCODE_ALGORITHM)
        decrypt_function = func.decrypt(
            decode_base64_function,
            db_crypt_key,
            settings.DB_CRYPT.ALGORITHM)

        return func.convert_from(
            decrypt_function,
            settings.DB_CRYPT.CONVERT_TO)
