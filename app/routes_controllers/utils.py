from flask import make_response
from flask import session as login_session
from app.models.models import User, Restaurant, MenuItem
from app.models.session_setup import export_db_session
import json

session = export_db_session()


def create_user(login_session):
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])

    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def json_response(message, server_code):

    """ Respond using JSON easily """

    response = make_response(json.dumps(message), server_code)
    response.headers['Content-Type'] = 'application/json'
    return response
