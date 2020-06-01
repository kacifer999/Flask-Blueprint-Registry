from flask_restplus import Api, Resource, Namespace
from flask import Blueprint, jsonify


def push_blueprint():
    return blueprint

blueprint = Blueprint('demo',__name__)
api = Api(blueprint,title='Demo')
ns_default = Namespace('default')
api.add_namespace(ns_default)

@ns_default.route('')
class Demo(Resource):
    def get(self):
        return jsonify(msg='This is a demo1.')
