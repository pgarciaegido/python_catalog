from flask import Flask


# ROUTES =====================================================================
from app.routes_controllers.auth import auth
from app.routes_controllers.auth_google import gauth
from app.routes_controllers.auth_facebook import fauth
from app.routes_controllers.categories import cat
from app.routes_controllers.item import item
from app.routes_controllers.api_json import api


app = Flask(__name__, template_folder='app/templates',
            static_folder='app/static')

app.register_blueprint(auth)
app.register_blueprint(gauth)
app.register_blueprint(fauth)
app.register_blueprint(cat)
app.register_blueprint(item)
app.register_blueprint(api)


# SERVER ======================================================================
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
