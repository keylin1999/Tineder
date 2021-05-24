# when a user sets up all its personal information
# and decide to pair an unknown person to chat
# maybe there will be some restriction if it is not
# ideal to pair in some condition:
#   if the person keeps sending pair request
#   if there is no suitable person to pair with it
# these conditions are also checked in this action

from model.chatroom import Chatroom
from model import db
from model.user import User
import sqlalchemy
from linebot.models import TextSendMessage
from typing import Tuple
from pair_logic.random_picker import RandomPicker
from action.pair_request_messages import get_message
from util.get_line_bot_api import line_bot_api

session_name = "pair"

def pair_user(user1_id:str, user2_id:str, db_session:sqlalchemy.orm.Session) -> None:
    user1 = db_session.query(User).filter_by(id=user1_id).first()
    user2 = db_session.query(User).filter_by(id=user2_id).first()
    if(user1 is None or user2 is None):
        if user1 is None:
            raise ValueError("user_id '" + user1_id + "' does not exist in database")
        else:
            raise ValueError("user_id '" + user2_id + "' does not exist in database")

    user1.paired_id = user2.id
    user2.paired_id = user1.id

    chatroom = Chatroom(
        user1_id        = user1_id,
        user2_id        = user2_id,
        image_enabled   = 0
    )
    db_session.add(chatroom)
    db_session.commit()

picker = RandomPicker()

def pair_request(user_state: dict,
                 user_id:str,
                 message: str,
                 session:sqlalchemy.orm.Session) -> Tuple[dict, TextSendMessage, bool]:
    
    paired_id = RandomPicker().pair(user_id=user_id,db_session=session)
    

    if paired_id is not None:
        return_message = get_message("pair_success")
        line_bot_api.push_message(to=paired_id, messages=TextSendMessage(text=get_message("sent_to_paired")))
    else:
        return_message = get_message("pair_fail")
    
    
    return_message = TextSendMessage(text=return_message)
    return_state = {}
    finished = True
    
    return return_state, return_message, finished



if __name__ == '__main__':
    from test_use.return_db import db
    session = db.session
    pair_user("2", "Uaa379e85866bc38e672bbf641d77bc60", session)
