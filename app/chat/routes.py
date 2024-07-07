from flask import Blueprint, request, session, jsonify, make_response
from datetime import datetime
from flask_socketio import emit, join_room, leave_room
from app import socketio

chat = Blueprint('chat', __name__)

@socketio.on('connect')
def handle_connect():
    if 'user_name' in session:
        join_room(session['user_name'])

@socketio.on('disconnect')
def handle_disconnect():
    if 'user_name' in session:
        leave_room(session['user_name'])

@socketio.on('send_message')
def handle_send_message(data):
    db = chat.app.db
    messages_collection = db["messages"]

    if session.get('login_status'):
        sender = session.get('user_name')
    else:
        message_count = int(request.cookies.get('message_count', 0))
        if message_count >= 3:
            chat_id = data.get('chat_id', 'default_chat')
            msg = "Signup/Login to enjoy unlimited free usage"
            data = {"sender": "You", "receiver": "ai", "message": msg, "chat_id": chat_id, 'usage_warning': 'limit_exceeded'}
            messages_collection.insert_one({"chat_id": chat_id, "sender": sender, "recipient": "ai", "message": msg, "timestamp": datetime.now()})
            emit('receive_message', data, room=chat_id)
            return

        session['message_count'] = str(message_count + 1)
        response = make_response()
        response.set_cookie("message_count", session.get('message_count'), max_age=60*60)
        sender = session['user_name']

    chat_id = data.get('chat_id', 'default_chat')
    room = chat_id

    msg = data['message']
    messages_collection.insert_one({"chat_id": chat_id, "sender": sender, "recipient": "ai", "message": msg, "timestamp": datetime.now()})

    # Here you would handle your message generation and translation
    # For the example, we will just echo the message back
    answer = f"Echo: {msg}"

    data_send = {"sender": "ai", "receiver": sender, "message": answer, "chat_id": chat_id}
    messages_collection.insert_one({"chat_id": chat_id, "sender": "ai", "recipient": sender, "message": answer, "timestamp": datetime.now()})
    emit('receive_message', data_send, room=room)
