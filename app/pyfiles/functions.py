import logging
from datetime import datetime

from app import db
from app.pyfiles.models import Message
from app.pyfiles.config import chat_length


def add_msg_to_db(user, message):
    """
    Function to add message of user to database

    :param user: username of sender
    :type user: str
    :param message: message of user
    :type message: str
    :return: None
    """
    msg = Message(user=user, message=message)
    try:
        db.session.add(msg)
        db.session.commit()
    except Exception as e:
        logging.warning('{} | There was an error. Could not add message to database | Error - {}'
                        .format(datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), str(e)))


def get_chat_history():
    """
    Function to get history of chat for limited amount of messages.
    You can change limit by setting your value for parameter 'chat_length' in config.py file

    :return: history of chat (list of dictionaries(keys - 'time', 'username', 'msg'))
    """
    sql_list = Message.query.all()[-chat_length:]
    history = [msg.get_info() for msg in sql_list]
    return history


def update_user_chat(first_user, second_user, data, user_chats):
    """
    Function to append new messages to user chat storage

    :param first_user: First user to update
    :type first_user: str
    :param second_user: Second user to update
    :type second_user: str
    :param data: Data that received from socket message (used to record properly sender of message)
    :type data: dict
    :param user_chats: dictionary of users and their private messages
    :type user_chats: dict
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


logging.basicConfig(filename='app/logs/logs.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')
