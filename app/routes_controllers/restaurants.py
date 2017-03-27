from flask import (Flask, render_template, request, redirect, url_for, jsonify,
                   flash, Blueprint)

from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Restaurant, Base, MenuItem

rest = Blueprint('restaurant', __name__, template_folder='templates')


# DB SETTINGS =================================================================
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@rest.route('/')
def showRestaurants():
    """ List all restaurants from db """
    print(login_session)
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@rest.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    """ GET: Renders a form to create a new restaurant
        POST: Stores new restaurant in db and redirects to root """
    if request.method == 'POST':
        name = request.form['name']
        new_restaurant = Restaurant(name=name)
        session.add(new_restaurant)
        session.commit()
        flash("New restaurant %s has been added" % name)
        return redirect('/')
    else:
        return render_template('new_restaurant.html')


@rest.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    """ GET: Renders form to edit restaurant name
        POST: Stores restaurant new name into db and redirects to its menu """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_name = request.form['name']
        restaurant.name = new_name
        session.commit()
        flash("Restaurant's new name is %s!" % new_name)
        return redirect(url_for('menu_items.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_restaurant.html', restaurant=restaurant)


@rest.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    """ GET: Renders page to ensure you want to delete restaurant
        POST: Deletes restaurant from db and redirects to root """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant has been deleted")
        return redirect(url_for('.showRestaurants'))
    else:
        return render_template('delete_restaurant.html', restaurant=restaurant)
