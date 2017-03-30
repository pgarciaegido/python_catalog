from flask import render_template, request, flash, Blueprint
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from utils import get_user_id, create_user, json_response


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

gauth = Blueprint('goauth', __name__, template_folder='templates')


@gauth.route('/gconnect', methods=['POST'])
def gconnect():

    """ Login with Google account:
        1. Validates state token with previously given. This happens in
           auth.py.
        2. Creates a credentials object, where access_token and id_token
           are given.
        3. Check that the access token is valid. It makes a request to google
           API, and aborts if JSON contains error
        4. Verify that the access token is used for the intended user. If user
           id given in credentials doesn't match with google id fetched in
           results variable, aborts.
        5. Verify that the access token is valid for this app. If issued_to
           attribute doesn't match with client_id (brought from secret.json
           file in root), aborts.
        6. Checks if user is already connected. If access_token and gplus_id
           have been created already and they are equal, returns a 200. If not
           they get registered into user session.
        7. Gets user info from google API and stores in his session the info.
        8. Checks for email into db. If doesn't exist, creates a new register.
        """

    # 1
    if request.args.get('state') != login_session['state']:
        return json_response('Invalid state parameter.', 401)
    # Obtain authorization code
    code = request.data

    # 2
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return json_response('Failed to upgrade the authorization code.', 401)

    # 3
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        return json_response('Error', 500)

    # 4
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return json_response("Token's user ID doesn't match given user ID.",
                             500)

    # 5
    if result['issued_to'] != CLIENT_ID:
        print "Token's client ID does not match app's."
        return json_response("Token's client ID does not match app's", 401)

    # 6
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return json_response('Current user is already connected.', 200)

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # 7
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # 8
    user_id = get_user_id(login_session['email'])
    if not user_id:
        # Creates user in DB and returns db id
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    return render_template('welcome.html')


@gauth.route('/gdisconnect')
def gdisconnect():

    """ Revokes google token for user. The rest of the logout happens on
        auth.py """

    access_token = login_session['access_token']
    if access_token is None:
        print 'Access Token is None'
        return json_response('Current user not connected.', 401)

    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        return json_response('Failed to revoke token for given user.', 400)
