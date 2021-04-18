from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from model import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#init
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

#load_model
# model = load_model()

#add_args
parser = reqparse.RequestParser()
parser.add_argument('message')
parser.add_argument('conversation_id')
class Conver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intent = db.Column(db.String(50))
    entity = db.Column(db.String(50))
    def __repr__(self):
        return '<Conver %s>' % self.intent
class ConverSchema(ma.Schema):
    class Meta:
        fields = ("id", "intent", "entity")
        model = Conver
conver_schema = ConverSchema()
convers_schema = ConverSchema(many= True)
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
class Init(Resource):
    def get(self):
        id = Conver.query.all()
        return convers_schema.dump(id) 

class Conversation(Resource):
    def get(self):
        pass
    def post(self):
        args = parser.parse_args()
        print (args['message'])
        intent = process_data(model, args['message'])
        print (intent)
        return {'intent' : str(intent)}
        # return {'message': args['message'], 'conversation_id': args['conversation_id']}
# Conver()
api.add_resource(Init, '/')
api.add_resource(Conversation, '/apis')
if __name__ == '__main__':
    app.run(debug=True)