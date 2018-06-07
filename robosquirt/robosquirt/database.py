from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from robosquirt.config import config


def get_sqlite_file_connection_url():
    return "sqlite:///{pth}/robosquirt.db".format(pth=config["sqlite_db_path"])


def get_engine():
    return create_engine(get_sqlite_file_connection_url())


session_factory = sessionmaker(bind=get_engine())
