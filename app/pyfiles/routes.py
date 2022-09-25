from flask import render_template, session, redirect, url_for, request, flash
from flask_socketio import send

from app import app, socketio
from app.pyfiles.functions import *


users = []
user_chats = {}


# Route to get main page
@app.route('/', methods=['GET'])
def index():
    if not session.get("username"):
        return redirect(url_for('login_page'))
    username = session.get('username')
    return render_template('index.html', username=username)


# Route to render login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('login')
        if username:
            if username in users:
                flash('User already in chat!')
                return render_template('login.html')
            session['username'] = username
            users.append(username)
            add_msg_to_db('Chat Events', 'User "{}" joined chat!'.format(username))
            chat_hist = get_chat_history()
            data = {'chatHistory': chat_hist, 'chatUsers': list(set(users))}
            socketio.send(data)
            return redirect(url_for('index'))
        flash('Enter login!')
        return render_template('login.html')
    if session.get('username') in users:
        return redirect(url_for('index'))
    return render_template('login.html')


# Route to logout
@app.route('/logout')
def logout():
    username = session.get('username')
    if username in users:
        users.remove(username)
    session.pop('username', None)
    if username in user_chats:
        user_chats.pop(username)
    add_msg_to_db('Chat Events', 'User "{}" left chat!'.format(username))
    chat_hist = get_chat_history()
    data = {'chatHistory': chat_hist, 'chatUsers': list(set(users))}
    socketio.send(data)
    return redirect(url_for('login_page'))


# Socket message handler
@socketio.on('message')
def handle_message(data):
    # Event on login
    if data['event'] == 'logged':
        username = session.get('username')
        users.append(username)
        chat_hist = get_chat_history()
        data = {'chatHistory': chat_hist, 'chatUsers': list(set(users)),
                'onlineChats': {user: list(user_chats[user]) for user in user_chats}}
        send(data, broadcast=True)
    # Event on sending message
    elif data['event'] == 'message':
        # Sending message to general chat
        if data['receiver'] == 'General chat':
            add_msg_to_db(data['username'], data['msg'])
            chat_hist = get_chat_history()
            data = {'chatHistory': chat_hist, 'chatUsers': list(set(users))}
            send(data, broadcast=True)
        # Sending message to user
        else:
            username = data['username']
            receiver = data['receiver']
            update_user_chat(username, receiver, data, user_chats)
            # Do not duplicates message if user sends message to himself
            if username != receiver:
                update_user_chat(receiver, username, data, user_chats)
            chat_hist = get_chat_history()
            data = {'chatHistory': chat_hist, 'chatUsers': list(set(users)), 'privateMsgTo': receiver,
                    'privateMsgFrom': username}
            send(data, broadcast=True)
    # Event to update data of private chats
    elif data['event'] == 'updateUserChat':
        username = session.get('username')
        chat_hist = get_chat_history()
        data = {'chatHistory': chat_hist, 'userChats': user_chats[username], 'chatUsers': list(set(users))}
        send(data)


# Socket disconnect handler. Pops out username of active users
@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in users:
        users.remove(username)
    chat_hist = get_chat_history()
    data = {'chatHistory': chat_hist, 'chatUsers': list(set(users))}
    socketio.send(data)
