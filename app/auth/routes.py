from flask import Blueprint, request, jsonify, session, redirect, url_for
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route("/signup", methods=["POST"])
def signup():
    db = auth.app.db
    users_collection = db["users"]

    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        return jsonify({"error": "Username or email already exists."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    users_collection.insert_one({"username": username, "email": email, "password": hashed_password})

    return jsonify({"message": "User registered successfully."})

@auth.route("/login", methods=["POST"])
def login():
    db = auth.app.db
    users_collection = db["users"]

    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = users_collection.find_one({"username": username})
    if user and bcrypt.check_password_hash(user["password"], password):
        session["user_name"] = username
        session['login_status'] = True
        return jsonify({"message": "Login successful."})
    else:
        return jsonify({"error": "Invalid username or password."}), 400
