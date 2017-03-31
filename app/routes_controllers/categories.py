from flask import (render_template, request, redirect, url_for, flash,
                   Blueprint)
from flask import session as login_session
# Imports db session
from app.models.session_setup import export_db_session
from app.models.models import Category, Item

cat = Blueprint('categories', __name__, template_folder='templates')
session = export_db_session()


@cat.route('/')
def showCategories():

    """ List all categories from db """

    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)
