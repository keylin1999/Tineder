from model.user import User
from typing import Tuple

import sqlalchemy

class PictureSetting:

    substate_name = "picture_setting"
    next_state_if_default = ""
    next_message_if_default = ""
    next_state_if_not_default = ""
    next_message_if_not_default = ""

    def __init__(self,
                 next_state_if_default,
                 next_message_if_default,
                 next_state_if_not_default,
                 next_message_if_not_default) -> None:
        
        self.next_state_if_default = next_state_if_default
        self.next_message_if_default = next_message_if_default
        self.next_state_if_not_default = next_state_if_not_default
        self.next_message_if_not_default = next_message_if_not_default
        
    def action(self,
               user_state: dict,
               user_id:str,
               message: str,
               session:sqlalchemy.orm.Session) -> Tuple[dict, str]:
        
        return_dict = {}


        if message['type'] == 'image_id':
            message = message['content']
            return_dict['image_id'] = message
            return_dict['substate'] = self.next_state_if_not_default
            reply_message = self.next_message_if_not_default

        elif message['type'] == 'text':
            message = message['content']
            user = session.query(User).filter_by(id=user_id).first()
            return_dict['substate'] = self.next_state_if_default 
            reply_message = self.next_message_if_default % user.status_message

        return return_dict, reply_message