from flask_restplus import Api, Resource, Namespace
from flask import Blueprint, jsonify



blueprint = Blueprint('demo',__name__)
api = Api(blueprint,title='Demo')


def push_blueprint():
    return blueprint


ns_demo = Namespace('default', description='Demo_Default_Function')
api.add_namespace(ns_demo)

@ns_demo.route('/')
class Demo(Resource):
    def get(self):
        return jsonify(msg='This is a demo.')
