from app import db
from datetime import datetime


class Message(db.Model):
    """Model for message
    Columns: message_id, user, message, time"""
    message_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(50))
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def get_info(self):
        return {'time': self.time.strftime('%H:%M:%S'), 'username': self.user, 'msg': self.message}

    def __repr__(self):
        return '<User %r>' % self.message_id
