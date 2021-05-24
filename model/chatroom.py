from . import db

class Chatroom(db.Model):
    __tablename__ = 'chatroom'

    # primary key
    user1_id        = db.Column(db.String(33), primary_key=True)
    user2_id        = db.Column(db.String(33), primary_key=True)

    # config
    image_enabled   = db.Column(db.Integer)

    def __init__(self,
                 user1_id         : int,
                 user2_id         : int,
                 image_enabled    : int = None) -> None:

        self.user1_id         = user1_id
        self.user2_id         = user2_id
        self.image_enabled    = image_enabled
        

