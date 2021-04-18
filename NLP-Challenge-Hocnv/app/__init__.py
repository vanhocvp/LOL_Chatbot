from flask import Flask
from config import Config
from model import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse, abort
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
model = load_model()
# model1 = model

id_request = 1
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('message')
parser.add_argument('conversation_id')
parser.add_argument('intent')
parser.add_argument('entity')

from app import models

conver_schema = models.ConverSchema()
convers_schema = models.ConverSchema(many= True)

from app import routes