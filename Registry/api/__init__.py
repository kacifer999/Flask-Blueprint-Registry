import os
import importlib
from flask import Flask, Blueprint, request, jsonify
from flask_restplus import Resource, Api, Namespace
from functions import *


app = Flask(__name__)


bp_admin = Blueprint('admin',__name__)
api = Api(bp_admin,title='Administration Apis')


ns_register = Namespace('register')
api.add_namespace(ns_register)
@ns_register.route('')
class Register(Resource):
    def post(self):
        # try:
        result = add_blueprint(app,request)
        # except:
            # return jsonify(status='500',message='Fail to register Api, someting went wrong.')
        return result


ns_unregister = Namespace('unregister')
api.add_namespace(ns_unregister)
@ns_unregister.route('/')
class UnRegister(Resource):
    def post(self):
        try:
        result = rm_blueprint(app,request)
        except:
            return jsonify(status='500',message='Fail to unregister Api, something went wrong')
        return result

ns_inquire = Namespace('inquire')
api.add_namespace(ns_inquire)
@ns_inquire.route('')
class Inquire(Resource):
    def get(self):
        try:
            result = inquire_blueprint(app)
        except:
            return jsonify(status='500',message='Fail to inquire Api, someting went wrong.')
        return result

ns_inquire_rm = Namespace('inquire_rm')
api.add_namespace(ns_inquire_rm)
@ns_inquire_rm.route('')
class Inquire_rm(Resource):
    def post(self):
        try:
            result = inquire_blueprint_rm(app,request)
        except:
            return jsonify(status='500',message='Fail to inquire Api, someting went wrong.')
        return result





def serve_app():
    print('Api Start Loading.')
    register_app(app,bp_admin,'/admin')
    print('Api Start Serving.')
    return app