from flask import Flask, Blueprint, request
from werkzeug.utils import import_string
from flask_restplus import Resource, Api, Namespace
from flask import jsonify
import importlib
app = Flask(__name__)

def register_app(app,blueprint,url_prefix):
    app.register_blueprint(blueprint,url_prefix=url_prefix)


def ok():   
    return jsonify(status='200',message='sucess')

def fail(msg):
    return jsonify(status='500',message=msg)



bp_admin = Blueprint('admin',__name__)
api = Api(bp_admin,title='Administration Apis')
ns_register = Namespace('register')
api.add_namespace(ns_register)


@ns_register.route('/')
class Register(Resource):
    def post(self):
        #init
        api_name = request.json['api_name']
        api_import_str = 'api.'+ api_name
        api_url = '/api/' + api_name

        try:
            #register
            blueprint = importlib.import_module(api_import_str).blueprint
            register_app(app,blueprint,api_url)
        except:
            return fail("Fail to register Api, 'api_name' is Occupied.")
        return ok()

ns_unregister = Namespace('unregister')
api.add_namespace(ns_unregister)

@ns_unregister.route('/')
class UnRegister(Resource):
    def post(self):
        #init
        api_name = request.json['api_name']

        try:
            # remove blueprint
            app.blueprints.pop(api_name)

            # remove routing rules from werkzeug.routing.Map
            view_rm_table = [key for key in app.view_functions.keys() if key.startswith(api_name + '.')]
            rule_rm_table = [key for key in app.url_map._rules_by_endpoint if key.startswith(api_name + '.')]
            [app.view_functions.pop(key) for key in view_rm_table]
            [app.url_map._rules_by_endpoint.pop(key) for key in rule_rm_table]
            app.url_map._rules = [rule for rule in app.url_map._rules if not rule.endpoint.startswith(api_name + '.')]
        except:
            return fail('Fail to unregister Api')
        return ok()


def serve_app():
    register_app(app,bp_admin,'/admin')
    return app