# when a person wants to unpair the handler
# will call this action

from linebot.models.send_messages import TextSendMessage
from requests.sessions import session
import sqlalchemy
from model.user import User
from util.get_line_bot_api import line_bot_api
from typing import Tuple

session_name = "unpair"

def unpair_user(user1_id:str, user2_id:str, db_session:sqlalchemy.orm.Session) -> None:
    #user1 is the user who request to unpair
    #user2 is the user who gets the message of being unpaired
    user1 = db_session.query(User).filter_by(id=user1_id).first()
    user2 = db_session.query(User).filter_by(id=user2_id).first()
    
    user1.paired_id = None
    user2.paired_id = None

    line_bot_api.push_message(
        user2_id,
        TextSendMessage(text="Your paired user has left the chatroom, find new person!")
    )
    db_session.commit()
    

def unpair_request(user_state: dict,
                   user_id:str,
                   message: str,
                   session:sqlalchemy.orm.Session) -> Tuple[dict, TextSendMessage, bool]:
    
    user1 = session.query(User).filter_by(id=user_id).first()
    if user1.paired_id is not None:
        unpair_user(user_id, user1.paired_id, session)

    if user1.activate == 1:
        return_message = TextSendMessage(text="You have successfully leave the chatroom")
    else:
        return_message = None

    return_state = {}
    finished = True
    return return_state, return_message, finished

if __name__ == '__main__':
    from test_use.return_db import db
    session = db.session
