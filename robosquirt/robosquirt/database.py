from configparser import NoSectionError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from robosquirt.config import config, get_project_root


def get_sqlite_file_connection_url():
    try:
        path = config.get("database", "sqlite_db_path") or str(get_project_root())
    except NoSectionError:
        path = str(get_project_root())
    return "sqlite:///{pth}/robosquirt.db".format(pth=path)


def get_engine():
    return create_engine(get_sqlite_file_connection_url())


session_factory = sessionmaker(bind=get_engine())
