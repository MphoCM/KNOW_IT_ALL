#!/usr/bin/env python3
# app/__init__.py
from flask import Flask
from firebase_admin import credentials, firestore, initialize_app
import json

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'KNOW-IT-ALL'

# Firebase initialization
cred = credentials.Certificate('serviceAccountKey.json')
initialize_app(cred)
db = firestore.client()

from app import routes
