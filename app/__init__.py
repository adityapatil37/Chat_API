from flask import Flask
from flask_bcrypt import Bcrypt
from flask_session import Session
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from flask_socketio import SocketIO

bcrypt = Bcrypt()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initialize MongoDB
    mongo_client = MongoClient('mongodb+srv://bosslog:bosslog@cluster0.wuhgfks.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', server_api=ServerApi('1'))
    app.db = mongo_client["Chat_API"]
    
    # Initialize Session management
    Session(app)

    # Register blueprints
    from app.main.routes import main
    from app.auth.routes import auth
    from app.chat.routes import chat
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(chat)
    
    # Initialize extensions
    bcrypt.init_app(app)
    socketio.init_app(app)
    
    return app
