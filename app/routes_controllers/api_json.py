from flask import (jsonify, Blueprint)

# Import db settings
from app.models.session_setup import export_db_session
from app.models.models import Category, Item


session = export_db_session()
api = Blueprint('api', __name__, template_folder='templates')


# API =========================================================================
@api.route('/categories/JSON')
def catalogJSON():

    """ Send all categories in JSON """

    categories = session.query(Category).all()
    return jsonify(Categories=[r.serialize for r in categories])


@api.route('/category/<int:category_id>/list/JSON')
def categoryItemsJSON(category_id):

    """ Send all items from a category in JSON """

    category = session.query(Category).filter_by(id=category_id).one()
    itms = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in itms])


@api.route('/category/<int:category_id>/list/<int:item_id>/JSON')
def itemJSON(category_id, item_id):

    """ Send an specific item info in JSON """

    item = session.query(Item).filter_by(category_id=category_id,
                                         id=item_id).one()
    return jsonify(Item=item.serialize)
