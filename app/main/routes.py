from flask import Blueprint, session, request, jsonify, redirect, url_for, make_response
from datetime import datetime

main = Blueprint('main', __name__)

@main.route("/index")
def ChatHome():
    db = main.app.db
    chat_instances_collection = db["chat_instances"]
    
    if session.get('login_status'):
        user_name = session['user_name']
        chat_instances = list(chat_instances_collection.find({"user": user_name}))
        return jsonify(chat_instances=chat_instances)
    else:
        if request.cookies.get('guest_id'):
            guest_id = request.cookies.get('guest_id')
            chat_instances = list(chat_instances_collection.find({"user": guest_id}))
            return jsonify(chat_instances=chat_instances)
        else:
            session['message_count'] = str(0)
            guest_id = f'guest-{datetime.now().timestamp()}'
            session['user_name'] = guest_id
            response = make_response(redirect(url_for('main.ChatHome')))
            response.set_cookie("guest_id", guest_id, max_age=60*60)
            response.set_cookie("message_count", session.get('message_count'), max_age=60*60)
            return response

@main.route("/new_chat")
def new_chat():
    db = main.app.db
    chat_instances_collection = db["chat_instances"]
    
    if session.get('login_status') or request.cookies.get('guest_id'):
        user_name = session['user_name']
        chat_id = f"chat_{datetime.now().timestamp()}"
        chat_instances_collection.insert_one({"user": user_name, "chat_id": chat_id, "created_at": datetime.now()})
        return jsonify(chat_id=chat_id)
    return redirect(url_for('main.ChatHome'))

@main.route("/chat/<chat_id>")
def ChatInstance(chat_id):
    db = main.app.db
    messages_collection = db["messages"]
    
    if 'user_name' in session or request.cookies.get('guest_id'):
        chat_history = list(messages_collection.find({"chat_id": chat_id}))
        user_name = session['user_name']
        chat_instances = list(db["chat_instances"].find({"user": user_name}))
        return jsonify(chat_history=chat_history, chat_instances=chat_instances)
    return redirect(url_for('main.ChatHome'))

@main.route("/logout")
def logout():
    session.clear()
    response = redirect(url_for("main.ChatHome"))
    response.set_cookie('guest_id', '', expires=0)
    response.set_cookie('message_count', '', expires=0)
    return response
