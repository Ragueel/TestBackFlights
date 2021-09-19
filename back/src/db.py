from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session
from .config import BaseConfig

def get_session_maker(config: BaseConfig):
    engine = create_engine(config.DB_CONNECTION)
    session_factory = sessionmaker(engine)
    Session = scoped_session(session_factory)
    return Session