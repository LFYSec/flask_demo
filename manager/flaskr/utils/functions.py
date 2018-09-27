from flask import Flask
import redis
import os

from App.models import db
from App.user_views import user_blueprint

def create_app():
	#system path
	BASE_DIR = os.path.dirname(__file__)
	#app
	app = Flask(__name__)
	#register blueprint
	app.register_blueprint(blueprint=user_blueprint,url_prefix='/user')
	#mysql
	app.config['SQLALCHEMY_DATABASE_URI'] = ''
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	#setting session
	app.config['SECRET_KEY'] = 'lfy123'
	app.config['SESSION_TYPE'] = 'redis'

	app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',port=6379)
	#init db
	db.init_app(app=app)

	return app