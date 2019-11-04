from flask_restplus import Api, Resource, Namespace
from flask import Blueprint, jsonify



blueprint = Blueprint('hello',__name__)
api = Api(blueprint,title='Hello World')


def push_blueprint():
    return blueprint


ns_demo = Namespace('default')
api.add_namespace(ns_demo)


@ns_demo.route('/')
class Demo(Resource):
    def get(self):
        return jsonify(msg='Hello World.')
