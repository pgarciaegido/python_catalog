from flask import (Flask)


# ROUTES =====================================================================
from app.routes_controllers.auth_google import auth
from app.routes_controllers.restaurants import rest
from app.routes_controllers.menu_item import item
from app.routes_controllers.api_json import api


app = Flask(__name__, template_folder='app/templates',
            static_folder='app/static')

app.register_blueprint(auth)
app.register_blueprint(rest)
app.register_blueprint(item)
app.register_blueprint(api)


# SERVER ======================================================================
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
