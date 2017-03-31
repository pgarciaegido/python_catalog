#  Yumm.py :poultry_leg:
Webapp where you can check a list of different categories and add new items or products if you are logged in. It has been developed using Flask and SQLite. This project is part of a Udacity course.

## Features
* Secure Social Login using your Google or Facebook account
* Create your own items in each category
* Edit and delete the items you have previously created
* API. Sends json formatted information about the db info.

## Structure
The project has a main file that serves the webapp and gather all the modules together: *catalog.py*. Inside the app folder, we can find the models, the routes and controllers, the static files and the templates.

## Usage
This project runs in Python, so first you will need to have it installed. I have used 2.7.13 to develop it. You'll also need SQLite.

Python packages used are sqlalchemy and Flask.

After cloning, a Vagrant folder is included in the repository, so you can launch a virtual machine with everything set up. (Courtesy of Udacity.) Just install Vagrant and Virtual Box. Then in the folder:

```sh
vagrant up
```

And to get inside the machine:
```sh
vagrant ssh
```
You should already be inside the machine.

In case you have troube with the database, you can generate a new file from the models:

```sh
python ./app/models/models.py
```


You can introduce some dummy information running the *lotsofitems.py* file.

```sh
python lotsofitems.py
```

To run the server (port 5000):

```sh
python catalog.py
```

For the social login to work, you should include your own *client_secrets.json* files from [Google](https://console.developers.google.com/apis/library?project=restaurant-menu-app-162814) and [Facebook](https://developers.facebook.com/) and place it in the root.

## Contributing

If you fancy, you can make a pull request and improve the functionality or even the UI of the site.

Any possible issues, you can report them [here](https://github.com/pgarciaegido/python_catalog/issues).


## Contact

You can contact me on pgarciaegido@gmail.com  :beer:
