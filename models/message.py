from . import db

""" This class defines the messages sent and received by the users. """
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())

    sender_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )

    def __repr__(self):
        return (f'<Message {self.body[:20]} from {self.sender_id} '
                f'to {self.receiver_id}>')
