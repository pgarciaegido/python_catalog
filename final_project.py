from flask import (Flask, render_template, request, redirect, url_for, jsonify,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)

# # # # # # # # # # # # # # # # # # # INDEX # # # # # # # # # # # # # # # # # #
# DB SETTINGS

# API ROUTES
# -- /restaurants/JSON                                 | restaurantsJSON()
# -- /restaurant/<restaurant_id>/menu/JSON             | restaurantMenuJSON()
# -- /restaurant/<restaurant_id>/menu/<menu_id>/JSON   | menuItemJSON()

# RENDER ROUTES
# -- /                                                 | showRestaurants()
# -- /restaurant/new                                   | newRestaurant()
# -- /restaurant/<restaurant_id>/edit                  | editRestaurant()
# -- /restaurant/<int:restaurant_id>/delete            | deleteRestaurant()
# -- /restaurant/<restaurant_id>                       | showMenu()
# -- /restaurant/<int:restaurant_id>/menu/new          | newMenuItem()
# -- /restaurant/<restaurant_id>/menu/<menu_id>/edit   | editMenuItem()
# -- /restaurant/<restaurant_id>/menu/<menu_id>/delete | deleteMenuItem()

# SERVER

# # # # # # # # # # # # # # # # # # # CODE # # # # # # # # # # # # # # # # # #

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


# RENDER ROUTES ===============================================================
@app.route('/')
def showRestaurants():
    """ List all restaurants from db """
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
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


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    """ GET: Renders form to edit restaurant name
        POST: Stores restaurant new name into db and redirects to its menu """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_name = request.form['name']
        restaurant.name = new_name
        session.commit()
        flash("Restaurant's new name is %s!" % new_name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    """ GET: Renders page to ensure you want to delete restaurant
        POST: Deletes restaurant from db and redirects to root """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant has been deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('delete_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
    """ Shows all menu items from a certain restaurant """
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('menu.html', items=items, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
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
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
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
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant=restaurant,
                               item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
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
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant=restaurant,
                               item=item)


# SERVER ======================================================================
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
