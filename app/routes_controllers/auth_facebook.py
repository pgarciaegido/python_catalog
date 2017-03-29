from flask import request, flash, Blueprint, make_response
from flask import session as login_session

import httplib2
import json

from utils import get_user_id, create_user, json_response


fauth = Blueprint('foauth', __name__, template_folder='templates')


@fauth.route('/fbconnect', methods=['POST'])
def fbconnect():

    """ Login using Facebook account:
        1. Compares login_session state with the one provided to template.
           This happens on auth.py
        2. Gets access_token from FB SDK (in the front). Check login.html
        3. Gets app id and app secret from secret fb JSON stored on root.
        4. Sets proper URL to fetch a new token. Make GET request, and
           make results readable handable (JSON). Then formates token.
        5. Sets url, make GET request, formates JSON, and asign new values
           to user session. The token must be stored in the login_session in
           order to properly logout.
        6. Similar to previous behaviour, in this case to get picture.
        7. Checks if user exists in local db. If it doesn't, it creates it.
           Also, user_id (from db) gets registered in user session.
        """

    # 1
    if request.args.get('state') != login_session['state']:
        return json_response('Invalid state parameter.', 401)

    # 2
    access_token = request.data

    # 3
    app_id = json.loads(
             open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
             open('fb_client_secrets.json', 'r').read())['web']['app_secret']

    # 4
    url = ('https://graph.facebook.com/v2.8/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    token = 'access_token=' + data['access_token']

    # 5
    url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    # Needed to logout
    login_session['facebook_id'] = data["id"]
    login_session['access_token'] = token

    # 6. GET PICTURE
    url = ('https://graph.facebook.com/v2.8/me/picture?%s'
           '&redirect=0&height=200&width=200') % token
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # 7. CHECK IF USER EXISTS
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


def fbdisconnect():

    """ Deletes access_token from facebook API making a delete request.
        The full disconnection happens on auth.py """

    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token'
           '=%s') % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"
