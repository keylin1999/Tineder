from typing import Tuple

import sqlalchemy
from util.get_line_bot_api import line_bot_api
from model.user import User
from util.get_image import get_image_content

class CheckPicture:

    substate_name = "check_picture"
    next_state_if_confirm = ""
    next_message_if_confirm = ""
    next_state_if_not_confirm = ""
    next_message_if_not_confirm = ""

    def __init__(self,
                 next_state_if_confirm,
                 next_message_if_confirm,
                 next_state_if_not_confirm,
                 next_message_if_not_confirm) -> None:
        
        self.next_state_if_confirm = next_state_if_confirm
        self.next_message_if_confirm = next_message_if_confirm
        self.next_state_if_not_confirm = next_state_if_not_confirm
        self.next_message_if_not_confirm = next_message_if_not_confirm
        
    def action(self,
               user_state: dict,
               user_id:str,
               message: str,
               session:sqlalchemy.orm.Session) -> Tuple[dict, str]:
        
        return_dict = {}

        # TODO save picture to the file

        if message == 'n':
            user_state.pop('image_id', None)
            return_dict['substate'] = self.next_state_if_not_confirm
            reply_message = self.next_message_if_not_confirm
        else:
            content_id = user_state['image_id']
            
            response = line_bot_api.get_message_content(content_id)
            user = session.query(User).filter_by(id=user_id).first()
            picture_id = user.picture_id
            get_image_content(content=response.content, id=picture_id)

            user = session.query(User).filter_by(id=user_id).first()

            return_dict['substate'] = self.next_state_if_confirm 
            reply_message = self.next_message_if_confirm % user.status_message

        return return_dict, reply_message