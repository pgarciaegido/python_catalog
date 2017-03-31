from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import Category, Base, Item, User
from app.models.session_setup import export_db_session

session = export_db_session()


# Create dummy user
User1 = User(name="Pablo Udacity", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Create Categories
Category1 = Category(name='Meat')
session.add(Category1)
session.commit()

Category2 = Category(name='Fish')
session.add(Category2)
session.commit()

Category3 = Category(name='Veggies')
session.add(Category3)
session.commit()

Category4 = Category(name='Drinks')
session.add(Category4)
session.commit()

Category5 = Category(name='Pasta')
session.add(Category5)
session.commit()

Category6 = Category(name='Rice')
session.add(Category6)
session.commit()

Category7 = Category(name='Eggs')
session.add(Category7)
session.commit()


# Creates items for categories
Item1 = Item(name='Beef', description="Some cool stuff", price="$ 3.00", category_id="1", user_id="1")
session.add(Item1)
session.commit()

Item2 = Item(name='Lamb', description="Some cool stuff", price="$ 4.00", category_id="1", user_id="1")
session.add(Item2)
session.commit()

Item3 = Item(name='Pork', description="Some cool stuff", price="$ 1.00", category_id="1", user_id="1")
session.add(Item3)
session.commit()

Item4 = Item(name='Salmon', description="Some cool stuff", price="$ 3.00", category_id="2", user_id="1")
session.add(Item4)
session.commit()

Item5 = Item(name='Onion', description="Some cool stuff", price="$ 4.00", category_id="3", user_id="1")
session.add(Item5)
session.commit()

Item6 = Item(name='Spaggeti', description="Some cool stuff", price="$ 1.00", category_id="5", user_id="1")
session.add(Item6)
session.commit()

Item7 = Item(name='Rum', description="Some cool stuff", price="$ 11.00", category_id="4", user_id="1")
session.add(Item7)
session.commit()

Item7 = Item(name='Special Indian Rice', description="Some cool stuff", price="$ 1.00", category_id="6", user_id="1")
session.add(Item7)
session.commit()

print "added items!"
