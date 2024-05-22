#!/usr/bin/env python3
import json
from flask import Flask
import firebase_admin
from firebase_admin import credentials


cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    from .views import main
    app.register_blueprint(main)

    return app
