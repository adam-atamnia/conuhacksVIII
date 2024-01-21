from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate('./credentials.json')

default_app = initialize_app(cred)

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '12345rtfescdvf'

  from userAPI import userAPI
  from statsAPI import statsAPI

  app.register_blueprint(userAPI, url_prefix='/user')
  app.register_blueprint(statsAPI, url_prefix='/stats')

  return app