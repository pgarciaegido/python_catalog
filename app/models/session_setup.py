from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Base, MenuItem


def export_db_session():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
