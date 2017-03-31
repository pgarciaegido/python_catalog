from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Base, Item


def export_db_session():
    engine = create_engine('sqlite:///catalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
