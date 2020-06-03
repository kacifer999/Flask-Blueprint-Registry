import os
import sys
import shutil
import importlib
from pathlib import Path
from flask import jsonify
# init
sandbox_root = 'api'
api_file_name = 'main.py'
api_root = Path(__file__).resolve().parent


def sucess(return_dict):
    return_dict.update({'status':'200','message':'sucess'})
    return jsonify(return_dict)

def fail(return_dict):
    return_dict.update({'status':'500'})
    return return_dict
    

def register_app(app,blueprint,url_prefix):
    app.register_blueprint(blueprint,url_prefix=url_prefix)


def add_blueprint(app,request):
    #init
    return_dict = {}
    project_id = request.json['project_id']
    sandbox_id = request.json['sandbox_id']
    sandbox_abs_dir = request.json['sandbox_abs_dir']
    sandbox_str = sandbox_root + '.'+ project_id + '.' + sandbox_id
    api_rel_url = '/' + sandbox_str.replace('.','/')
    sandbox_dir = api_root.joinpath(sandbox_str.replace('.',os.sep))

    # blueprint check
    if  sandbox_id in app.blueprints:
        return_dict.update({'message':'Fail to register Api, ' + str(sandbox_id) + ' occupied'})
        return fail(return_dict)

    # API file check
    if not sandbox_dir.joinpath(api_file_name).exists():
        return_dict.update({'message':'Fail to register Api, file not exists.'})
        return fail(return_dict)

    # copy __init__
    if not sandbox_dir.joinpath('__init__.py').exists():
        shutil.copy(api_root.joinpath('template').joinpath('__init__.py'),sandbox_dir.joinpath('__init__.py'))
    
    # register
    module = importlib.import_module(sandbox_str)
    importlib.reload(sys.modules.get(module.blueprint().import_name))
    blueprint = module.blueprint()
    register_app(app,blueprint,api_rel_url)

    bp_list = list(app.blueprints.keys())
    if sandbox_id not in bp_list:
        return_dict.update({'message':'Fail to register Api,sandbox_id not in bp_list, someting went wrong.'})
        return fail(return_dict)

    return_dict.update({'sandbox_rel_url':api_rel_url})
    del module
    return sucess(return_dict)
    

def rm_blueprint(app,request):

    # init
    return_dict = {}
    blueprint_id = request.json['sandbox_id']
    # check sandbox_id
    if blueprint_id not in app.blueprints:
        return_dict.update({'message':'Fail to unregister Api, ' + str(blueprint_id) + ' is not running'})
        return fail(return_dict)

    # remove blueprint object form app.blueprints list
    rm_blueprint_id = app.blueprints.pop(blueprint_id)
    del rm_blueprint_id

    # remove blueprint's view function object  app.view_functions dict
    for rm_view_key in list(app.view_functions):
        if rm_view_key.startswith(blueprint_id + '.'):
            rm_view_id = app.view_functions.pop(rm_view_key)
            del rm_view_id

    # remove routing rules from app.url_map==werkzeug.routing.Map
    [app.url_map._rules_by_endpoint.pop(key) for key in list(app.url_map._rules_by_endpoint) if key.startswith(blueprint_id + '.')]
    app.url_map._rules = [rule for rule in app.url_map._rules if not rule.endpoint.startswith(blueprint_id + '.')]
    return sucess(return_dict)

def inquire_blueprint_internal(app):
    vanilla_bp = ['admin','restplus_doc']
    bp_list = list(app.blueprints.keys())
    [bp_list.remove(item) for item in vanilla_bp]
    return bp_list

def inquire_blueprint(app):
    return_dict = {}
    bp_list = inquire_blueprint_internal(app)
    return_dict.update({'api_list':bp_list})
    return sucess(return_dict)

# def inquire_blueprint_rm(app,request):
#     # init
#     return_dict = {}
#     sandbox_id = request.json['sandbox_id']
#     return_dict.update({'sandbox_id':sandbox_id})
#     return_dict.update({'bp_list':list(app.blueprints.keys())})

#     # remove blueprint list
#     try:
#         app.blueprints.pop(sandbox_id)
#     except:
#         return_dict.update({'reason1':'pop from bp failed.'})

    
    

#     # remove routing rules from werkzeug.routing.Map
#     view_rm_table = [key for key in app.view_functions.keys() if key.startswith(sandbox_id + '.')]
#     rule_rm_table = [key for key in app.url_map._rules_by_endpoint if key.startswith(sandbox_id + '.')]
#     return_dict.update({'view_functions':list(app.view_functions.keys())})
#     return_dict.update({'view_rm_table':view_rm_table})
#     return_dict.update({'rule_table':list(app.url_map._rules_by_endpoint)})
#     return_dict.update({'rule_rm_table':rule_rm_table})

#     try:
#         [app.view_functions.pop(key) for key in view_rm_table]
#     except:
#         return_dict.update({'reason2':'pop from view failed.'})
    
#     try:
#         [app.url_map._rules_by_endpoint.pop(key) for key in rule_rm_table]
#         app.url_map._rules = [rule for rule in app.url_map._rules if not rule.endpoint.startswith(sandbox_id + '.')]
#     except:
#         return_dict.update({'reason3':'pop from rule failed.'})

#     return_dict.update({'new_rules':list(app.url_map._rules_by_endpoint)})

#     return sucess(return_dict)