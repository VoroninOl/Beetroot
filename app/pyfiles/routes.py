import random
from flask import render_template, session, redirect, url_for, request, flash
from flask_socketio import send

from app import app, socketio
# from app import app, login_manager

users = set()
chat_hist = []


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
            chat_hist.append({'username': 'Chat Events', 'msg': 'User "{}" joined chat!'.format(username)})
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
    chat_hist.append({'username': 'Chat Events', 'msg': 'User "{}" left chat!'.format(username)})
    data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
    socketio.send(data)
    return redirect(url_for('login_page'))


@socketio.on('message')
def handle_message(data):
    print(data)
    # messages = {i: random.randint(5, 30) for i in range(15)}
    # data =
    if data['event'] == 'logged':
        username = session.get('username')
        users.add(username)
        data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
        send(data, broadcast=True)
    elif data['event'] == 'generalMessage':
        chat_hist.append({'username': data['username'], 'msg': data['msg']})
        username = session.get('username')
        data = {'chatHistory': chat_hist, 'chatUsers': list(users)}
        send(data, broadcast=True)

