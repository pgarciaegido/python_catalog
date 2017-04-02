from flask import (render_template, request, redirect, url_for, flash,
                   Blueprint)
from flask import session as login_session
# Imports db session
from app.models.session_setup import export_db_session
from app.models.models import Category, Item

session = export_db_session()
item = Blueprint('items', __name__, template_folder='templates')


@item.route('/category/<int:category_id>')
def showCategory(category_id):

    """ Shows all items from a certain category """

    # Checks if there is such a category
    try:
        category = session.query(Category).filter_by(id=category_id).one()
    except:
        return 'Category does not exist!'

    items = session.query(Item).filter_by(category_id=category_id).all()

    return render_template('items.html', items=items, category=category)


@item.route('/category/<int:category_id>/menu/new',
            methods=['GET', 'POST'])
def newItem(category_id):

    """ GET: Renders form to create new item
        POST: Stores new item into db and redirects to category list """

    # Checks if there is such a category
    try:
        category = session.query(Category).filter_by(id=category_id).one()
    except:
        return 'Category does not exist!'

    # Current user (if there is one) is not the creator
    if not login_session:
        return 'User not identified. Access denied'

    if request.method == 'POST':

        name = request.form['name']
        new_item = Item(name=name,
                        description=request.form['description'],
                        price=request.form['price'],
                        category_id=category_id,
                        user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()
        flash("New item %s has been added" % name)
        return redirect(url_for('.showCategory', category_id=category_id))
    else:
        return render_template('new_item.html', category=category)


@item.route('/category/<int:category_id>/list/<int:item_id>/edit',
            methods=['GET', 'POST'])
def editItem(category_id, item_id):

    """ GET: Renders form to edit menu item
        POST: Stores new menu item info and redirects to category menu """

    # Checks if there is such a category
    try:
        category = session.query(Category).filter_by(id=category_id).one()
    except:
        return 'Category does not exist!'

    # Checks if there is such an item
    try:
        item = session.query(Item).filter_by(id=item_id).one()
    except:
        return 'Item does not exist!'

    # Current user (if there is one) is not the creator
    try:
        logged_user = login_session['user_id']
    except:
        return 'User not identified. Access denied'

    if logged_user != item.user_id:
        return 'User not identified. Access denied'

    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        session.commit()
        flash("Item has been edited!")
        return redirect(url_for('.showCategory', category_id=category_id))
    else:
        return render_template('edit_item.html', category=category, item=item)


@item.route('/category/<int:category_id>/list/<int:item_id>/delete',
            methods=['GET', 'POST'])
def deleteItem(category_id, item_id):

    """ GET: Renders page to ensure you want to delete item
        POST: Deletes item into db and redirects to category list """

    # Checks if there is such a category
    try:
        category = session.query(Category).filter_by(id=category_id).one()
    except:
        return 'Category does not exist!'

    # Checks if there is such an item
    try:
        item = session.query(Item).filter_by(id=item_id).one()
    except:
        return 'Item does not exist!'

    # Current user (if there is one) is not the creator
    try:
        logged_user = login_session['user_id']
    except:
        return 'User not identified. Access denied'

    if logged_user != item.user_id:
        return 'User not identified. Access denied'

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('.showCategory', category_id=category_id))
    else:
        return render_template('delete_item.html', category=category,
                               item=item)
