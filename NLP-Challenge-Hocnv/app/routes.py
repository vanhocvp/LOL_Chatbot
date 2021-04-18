from app import *
from app.models import *
from model import *
from flask_restful import Resource, Api, reqparse, abort, request
from flask import send_file, jsonify
import flask
import io
import base64
import redis
from typing import Any
import time
# model = load_model()
# red = redis.StrictRedis(host='localhost',
#                         port=6379,
#                         db=0)
# red.flushdb()
class ConverSchema(ma.Schema):
    class Meta:
        fields = ("conversation_id", "intent", "hero", "skill","action")
        model = Conver 
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
class Init(Resource):
    #return conversation_id
    def get(self):
        x = Conver(intent = "", hero = "", skill = "")
        db.session.add(x)
        db.session.commit()
        return {'conversation_id':str(x.conversation_id)}

class Conversation(Resource):
    def get(self):
        pass   
    def post(self):
        global id_request
        id_request += 1
        args = request.json
        print (type(args))
        # args = json.loads(args)
        args['coversation_id'] = str(args['conversation_id'])
        # print (args)
        # print (type(args))
        response = process_request(args, model)
        return jsonify(response)
        param = {}
        param['conversation_id'] = args['conversation_id']
        param['message'] = args['message']
        param['id_request'] = id_request
        args = json.dumps(param)
        if red.get('new_request_worker_1') == None:
            red.set('new_request_worker_1', str(False))
        # if red.get('have_response_worker_1') == None:
        #     red.set('have_response_worker_1', str(False))
        is_used_1 = not str_to_bool(red.get("new_request_worker_1"))
        if is_used_1:
            red.set('request_worker_1', args)
            red.set('new_request_worker_1', str(True))
        while(True):
            try:
                response = red.get('response_worker_1')
                response = json.loads(response)
                mess = response['response']
                id = response['id_request']
                if id == id_request:
                    return jsonify(mess)
                response = red.get('response_worker_2')
                response = json.loads(response)
                mess = response['response']
                id = response['id_request']
                if id == id_request:
                    return jsonify(mess)
            except:
                continue
            # if str_to_bool(red.get("have_response_worker_1")) == True:
            #     red.set('have_response_worker_1', str(False))
            #     response = red.get('response_worker_1')
            #     response = json.loads(response)
            #     mess = response['response']
            #     id = response['id_request']
            #     if id == id_request:
            #         return jsonify(mess)
# Conver()
def str_to_bool(s):
    if s == b'True':
        return True
    if s == b'False':
        return False
    return False

conver_schema = ConverSchema()
convers_schema = ConverSchema(many= True)
api.add_resource(Init, '/apis/init')
api.add_resource(Conversation, '/apis/conversation')
