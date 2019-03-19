# project/server/auth/views.py
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from operator import itemgetter
from project.server import bcrypt, db
import requests
from project.server.models import User, BlacklistToken,UserPage

from . import db as d

auth_blueprint = Blueprint('auth', __name__)
class UserPageRegister(MethodView):
    def post(self):
        post_data = request.get_json()
        # check if user already exists
        userpage = UserPage.query.filter_by(id_page=post_data.get('id_page'),id_user=post_data.get('id_user')).first()
        if not userpage:
            try:
                userpage = UserPage(
                    id_user=post_data.get('id_user'),
                    id_page=post_data.get('id_page'),
                    numberV=1
                )
                # insert the user
                db.session.add(userpage)
                db.session.commit()
                # generate the auth token
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully added.'
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            userpage.numberV=userpage.numberV+1
            db.session.add(userpage)
            db.session.commit()
            responseObject = {
                'status': 'succes',
                'message': 'Updated',
            }
            return make_response(jsonify(responseObject)), 202


class Moteur(MethodView):
    def post(self):
        post_data = request.get_json()
        id=post_data.get('id')
        user = User.query.filter_by(
                id=post_data.get('id')
            ).first()
        users= User.query.filter_by(
                profession=user.profession
            )
        #=from authentication
        userpages=UserPage.query.filter_by(id_user=id)
        list_pagev=[]
        for p in userpages:
            list_pagev.append(p.id_page)
        page_f=[]
        list_id=set()
        for user in users:
            line_user=UserPage.query.filter_by(id_user=str(user.id))
            vector=[]
            for col in line_user:
                vector.append((col.id_page,col.numberV))
                list_id.add(col.id_page)
            page_f.extend(vector)
        page_score=[]
        for id in list_id:
            if id not in list_pagev:
                score=0
                for tpl in page_f:
                    if tpl[0]==id:
                        score=score+tpl[1]
                page_score.append((id,score))
        list_r=[]
        
        for page in page_score:

            vector=d.findVectorOfOneDocument("servicepublic","corpus","mongodb://localhost:27017",page[0])
            list_r.append({"titre":vector["name"],"url":vector["url"]})

        return make_response(jsonify({"link":list_r[:10]})), 202

    
class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    first_name=post_data.get('first_name'),
                    last_name=post_data.get('last_name'),
                    profession=post_data.get('profession')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

class LoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
                ):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token.decode()
                        }
                        return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500

class UserAPI(MethodView):
    """
    User Resource
    """
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on,
                         'profession':user.profession
                    }
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403


# define the API resources
registration_pageview = UserPageRegister.as_view('register_pageview')
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')
moteur=Moteur.as_view('moteur')

# add Rules for API Endpoints

auth_blueprint.add_url_rule(
    '/viewpage/register',
    view_func=registration_pageview,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/viewpage/pages',
    view_func=moteur,
    methods=['POST']
)


auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)