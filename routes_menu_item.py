from flask import (Flask, render_template, request, redirect, url_for, jsonify,
                   flash, Blueprint)

from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

item = Blueprint('item', __name__, template_folder='templates')

# DB SETTINGS =================================================================
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

item = Blueprint('menu_items', __name__, template_folder='templates')


@item.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
    """ Shows all menu items from a certain restaurant """
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('menu.html', items=items, restaurant=restaurant)


@item.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """ GET: Renders form to create new menu item
        POST: Stores new menu item into db and redirects to restaurant menu """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        name = request.form['name']
        new_item = MenuItem(name=name,
                            description=request.form['description'],
                            price=request.form['price'],
                            course=request.form['course'],
                            restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New menu item %s has been added" % name)
        return redirect(url_for('.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant=restaurant)


@item.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
            methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    """ GET: Renders form to edit menu item
        POST: Stores new menu item info and redirects to restaurant menu """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.course = request.form['course']
        session.commit()
        flash("Menu item has been edited!")
        return redirect(url_for('.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant=restaurant,
                               item=item)


@item.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
            methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    """ GET: Renders page to ensure you want to delete item
        POST: Deletes menu item into db and redirects to restaurant menu """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu item has been deleted!")
        return redirect(url_for('.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant=restaurant,
                               item=item)
