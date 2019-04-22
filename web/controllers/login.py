import datetime
import json
import requests

from flask import flash, redirect, render_template, request, url_for, session

from web import app
from web.models import *
import web.config as config
from web.models.user import *
from web.utils import *
from web.constants import *

# https://scotch.io/tutorials/authentication-and-authorization-with-flask-login
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Compute redirect url
    if 'redirect' in request.args:
        redirect_url = config.DOMAIN+'/login?redirect=' + request.args['redirect']
    else:
        redirect_url = config.DOMAIN+'/login'

    # Check if already logged in
    if 'jwt' in request.cookies:
        print('jwt')
        try:
            id = decode_token(request.cookies['jwt'])
            user = User.query.filter_by(id=id).first()
            return redirect('/')
        except Exception as e:
            pass

    try:
        print(request.args)
    except Exception as e:
        print(e)


    return render_template('login.html')

# @app.route('/login')
# def login_page():
#     # Compute redirect url
#     if 'redirect' in request.args:
#         redirect_url = config.DOMAIN+'/login?redirect=' + request.args['redirect']
#     else:
#         redirect_url = config.DOMAIN+'/login'

#     if 'jwt' in request.cookies:
#         try:
#             id = decode_token(request.cookies['jwt'])
#             user = User.query.filter_by(id=id).first()
#             return redirect('/')
#         except Exception as e:
#             pass

#     client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
#     error = ""

#     try:
#         print('Hello')
#         if "code" in request.args and "state" in request.args and request.args['state'] == session['state']:
#             r = requests.post('https://oidc.mit.edu/token', 
#                 auth=requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), 
#                 data={"grant_type": "authorization_code","code": request.args["code"],"redirect_uri": redirect_url})
#             auth_token = json.loads(r.text)["access_token"]
#             r = requests.get('https://oidc.mit.edu/userinfo', headers={"Authorization": "Bearer " + auth_token})
#             user_info = json.loads(r.text)
#             if "email" in user_info and user_info["email_verified"] == True and user_info["email"].endswith("@mit.edu"):
#                 # Authenticated
#                 email = user_info["email"]
#                 name = user_info["name"]

#                 user = User.query.filter_by(email=email).first()
#                 if user is None:
#                     # Initialize the user with a very old last_post time
#                     user = User(email=email, name=name, last_post=datetime.datetime.min)
#                     db.session.add(user)
#                     db.session.commit()

#                 token = encode_token(user)
#                 response = app.make_response(redirect('/'))
#                 if 'redirect' in request.args:
#                     response = app.make_response(redirect(request.args['redirect']))

#                 response.set_cookie('jwt', token, expires=datetime.datetime.now()+datetime.timedelta(days=90))
#                 return response
#             else:
#                 if not "email" in user_info:
#                     error = "We need your email to work."
#                 else:
#                     error = "Invalid Login."
            
#             session["state"] = rndstr()
#             session["nonce"] = rndstr()

#             args = {
#                 "client_id": CLIENT_ID,
#                 "response_type": ["code"],
#                 "scope": ["email", "openid", "profile"],
#                 "state": session["state"],
#                 "nonce": session["nonce"],
#                 "redirect_uri": redirect_url
#             }

#             auth_req = client.construct_AuthorizationRequest(request_args=args)
#             login_url = auth_req.request('https://oidc.mit.edu/authorize')

#             if error == "":
#                 return redirect(login_url)
#             else:
#                 return render_template('error.html', login_url=login_url, error=error)
#     except Exception as e:
#         session["state"] = rndstr()
#         session["nonce"] = rndstr()

#         args = {
#             "client_id": CLIENT_ID,
#             "response_type": ["code"],
#             "scope": ["email", "openid", "profile"],
#             "state": session["state"],
#             "nonce": session["nonce"],
#             "redirect_uri": config.DOMAIN+'/login'
#         }

#         auth_req = client.construct_AuthorizationRequest(request_args=args)
#         login_url = auth_req.request('https://oidc.mit.edu/authorize')

#         return render_template('error.html', login_url=login_url, error="Stuff didn't go according to plan :(")
