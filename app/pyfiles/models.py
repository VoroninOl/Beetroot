from app import db
from flask_login import UserMixin
from datetime import datetime


class Message(db.Model, UserMixin):
    """Model for message
    Columns: message_id, user, message"""
    message_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(50))
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.message_id
