from flask import (jsonify, Blueprint)

# Import db settings
from app.models.session_setup import export_db_session
from app.models.models import Restaurant, MenuItem


session = export_db_session()
api = Blueprint('api', __name__, template_folder='templates')


# API =========================================================================
@api.route('/restaurants/JSON')
def restaurantsJSON():

    """ Send all restaurants in JSON """

    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@api.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):

    """ Send all menu items from a restaurant in JSON """

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itms = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in itms])


@api.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):

    """ Send an specific menu item info in JSON """

    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                             id=menu_id).one()
    return jsonify(MenuItem=item.serialize)
