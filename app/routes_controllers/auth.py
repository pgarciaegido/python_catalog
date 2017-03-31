from flask import flash, Blueprint, redirect, url_for, render_template
from flask import session as login_session
from auth_google import gdisconnect
from auth_facebook import fbdisconnect

import random
import string


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login')
def showLogin():

    """ Renders login template. For security reasons, create state that
        is checked on login."""

    # Creates a 32 string long using upercase chars and digits
    state = ''.join(random.choice(string.ascii_uppercase + string.
                                  digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Disconnect based on provider
@auth.route('/disconnect')
def disconnect():

    """ Logs out and delete user session and FB or GOOGLE tokens """

    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            # Special google session elements
            del login_session['gplus_id']
            del login_session['access_token']

        if login_session['provider'] == 'facebook':
            fbdisconnect()
            # Special fb session elements
            del login_session['facebook_id']

        # General login_session elements
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        flash("You have successfully been logged out.")
        return redirect(url_for('categories.showCategories'))

    else:
        flash("You were not logged in")
        return redirect(url_for('categories.showCategories'))
