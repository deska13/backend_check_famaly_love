from sqlalchemy import create_engine
from core import PostgresSetting
from sqlalchemy_utils import database_exists, create_database


def create_database():
    postgres_setting = PostgresSetting(_env_file='config/postgres.env')
    engine = create_engine(postgres_setting.postgres_sync_connect)
    if not database_exists(engine.url):
        print('Создание базы данных')
        create_database(engine.url)
    print(database_exists(engine.url))


create_database()