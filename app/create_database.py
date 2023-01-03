from sqlalchemy import create_engine
from core import PostgresSetting
from sqlalchemy_utils import database_exists, create_database
from models.database._base import BaseOrmModel
import models.database


def create_postgre_database():
    postgres_setting = PostgresSetting(_env_file='config/postgres.env')
    engine = create_engine(postgres_setting.postgres_sync_connect)
    if not database_exists(engine.url):
        print(f'Создание базы данных {engine.url}')
        create_database(engine.url)
        BaseOrmModel.metadata.create_all(engine)
    print(database_exists(engine.url))


create_postgre_database()
