from flask import (render_template, request, flash, Blueprint, make_response)
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from utils import get_user_id, create_user


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

gauth = Blueprint('goauth', __name__, template_folder='templates')


def json_response(message, server_code):
    response = make_response(json.dumps(message), server_code)
    response.headers['Content-Type'] = 'application/json'
    return response


# Create a state token to prevent request forgery
# Store it in the session for later validation
@gauth.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
                                  digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@gauth.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        return json_response('Invalid state parameter.', 401)
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return json_response('Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return json_response('Error', 500)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return json_response("Token's user ID doesn't match given user ID.",
                              500)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        print "Token's client ID does not match app's."
        return json_response("Token's client ID does not match app's", 401)

    stored_access_token = login_session.get('access_token')
    print(stored_access_token)
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return json_response('Current user is already connected.', 200)

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Searches for email in DB
    user_id = get_user_id(login_session['email'])
    if not user_id:
        # Creates user in DB and returns db id
        login_session['id'] = create_user(login_session)


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@gauth.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        return json_response('Current user not connected.', 401)

    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['id']
        return json_response('Succesfully disconnected.', 200)
    else:
        return json_response('Failed to revoke token for given user.', 400)
