import json
from os import path

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    with open(path.join("data", "settings.json")) as file:
        conn_data = json.load(file)

    conn_str = f'postgresql://{conn_data["pguser"]}:{conn_data["pgpassword"]}@{conn_data["pghost"]}:{conn_data["pgport"]}/{conn_data["pgdb"]}'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()