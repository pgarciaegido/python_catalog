from flask import (Flask, render_template, request, redirect, url_for, jsonify,
                   flash)

from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import Restaurant, MenuItem, Base

# ROUTES =====================================================================
from app.routes_controllers.auth_google import auth
from app.routes_controllers.restaurants import rest
from app.routes_controllers.menu_item import item

app = Flask(__name__, template_folder='app/templates')
app.register_blueprint(auth)
app.register_blueprint(rest)
app.register_blueprint(item)

# DB SETTINGS =================================================================
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# API =========================================================================
@app.route('/restaurants/JSON')
def restaurantsJSON():
    """ Send all restaurants in JSON """
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    """ Send all menu items from a restaurant in JSON """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    """ Send an specific menu item info in JSON """
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                             id=menu_id).one()
    return jsonify(MenuItem=item.serialize)



# SERVER ======================================================================
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
