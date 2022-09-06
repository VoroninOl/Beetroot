from flask import render_template, session, redirect, url_for, request, flash
from flask_socketio import send
from datetime import datetime

from app import app, socketio


def update_user_chat(first_user, second_user, data):
    """
    Function to append new messages to user chat storage

    :param first_user: First user to update
    :type first_user: str
    :param second_user: Second user to update
    :type second_user: str
    :param data: Data that received from socket message (used to record properly sender of message)
    :type data: dict
    :return: None
    """
    if first_user not in user_chats:
        user_chats[first_user] = {second_user: [{'username': data['username'], 'msg': data['msg'],
                                                 'time': datetime.utcnow().strftime('%H:%M:%S')}]}
    elif second_user not in user_chats[first_user]:
        user_chats[first_user][second_user] = [{'username': data['username'], 'msg': data['msg'],
                                                'time': datetime.utcnow().strftime('%H:%M:%S')}]
    else:
        user_chats[first_user][second_user].append({'username': data['username'], 'msg': data['msg'],
                                                    'time': datetime.utcnow().strftime('%H:%M:%S')})


users = set()
chat_hist = []
user_chats = {}


# Route of main page
@app.route('/', methods=['GET'])
def index():
    if not session.get("username"):
        return redirect(url_for('login_page'))
    username = session.get('username')
    return render_template('index.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('login')
        if username:
            session['username'] = username
            users.add(username)
            chat_hist.append({'username': 'Chat Events', 'msg': 'User "{}" joined chat!'.format(username),
                              'time': datetime.utcnow().strftime('%H:%M:%S')})
            data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
            socketio.send(data)
            return redirect(url_for('index'))
        flash('Enter login!')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    username = session.get('username')
    try:
        users.remove(username)
    except Exception as ex:
        print('Error in user logging out | {}'.format(ex))
    session.pop('username', None)
    user_chats.pop(username)
    chat_hist.append({'username': 'Chat Events', 'msg': 'User "{}" left chat!'.format(username),
                      'time': datetime.utcnow().strftime('%H:%M:%S')})
    data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
    socketio.send(data)
    return redirect(url_for('login_page'))


@socketio.on('message')
def handle_message(data):
    if data['event'] == 'logged':
        username = session.get('username')
        users.add(username)
        data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
        send(data, broadcast=True)
    elif data['event'] == 'message':
        if data['receiver'] == 'General chat':
            chat_hist.append({'username': data['username'], 'msg': data['msg'],
                              'time': datetime.utcnow().strftime('%H:%M:%S')})
            data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
            send(data, broadcast=True)
        else:
            username = data['username']
            receiver = data['receiver']
            update_user_chat(username, receiver, data)
            if username != receiver:
                update_user_chat(receiver, username, data)
            data = {'chatHistory': chat_hist, 'chatUsers': list(users), 'privateMsgTo': receiver,
                    'privateMsgFrom': username}
            send(data, broadcast=True)
    elif data['event'] == 'updateUserChat':
        username = session.get('username')
        # check if need check user in dict
        data = {'chatHistory': chat_hist, 'userChats': user_chats[username], 'chatUsers': list(users)}
        send(data)


@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    try:
        users.remove(username)
    except Exception as ex:
        print('Error in user logging out | {}'.format(ex))
    data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
    socketio.send(data)
