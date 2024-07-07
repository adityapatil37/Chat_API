import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    MONGODB_URI = os.environ.get('MONGODB_URI', )
    SESSION_MONGODB = MongoClient('mongodb+srv://bosslog:bosslog@cluster0.wuhgfks.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', server_api=ServerApi('1'))
    SESSION_TYPE = 'mongodb'
    SESSION_MONGODB_DB = 'Chat_API'
    SESSION_MONGODB_COLLECTION = 'sessions'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600 
