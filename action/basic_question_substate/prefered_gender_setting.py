from model.user import User
from typing import Tuple

import sqlalchemy

class PreferedGenderSetting:

    substate_name = "prefered_gender_setting"
    next_state_if_valid_data = ""
    next_message_if_valid_data = ""
    next_state_if_invalid_data = ""
    next_message_if_invalid_data = ""

    def __init__(self,
                 next_state_if_valid_data,
                 next_message_if_valid_data,
                 next_state_if_invalid_data,
                 next_message_if_invalid_data) -> None:
        self.next_state_if_valid_data     = next_state_if_valid_data
        self.next_message_if_valid_data   = next_message_if_valid_data
        self.next_state_if_invalid_data   = next_state_if_invalid_data
        self.next_message_if_invalid_data = next_message_if_invalid_data
    
    def action(self,
               user_state: dict,
               user_id:str,
               message: str,
               session:sqlalchemy.orm.Session) -> Tuple[dict, str]:

        return_dict = {}
        
        if message['type'] == 'text':
            message = message['content']
            if message != "female" and message != "male":
                match = False
            else:
                match = True

            if match:
                user = session.query(User).filter_by(id=user_id).first()
                user.prefered_gender = message
                session.commit()
                return_dict['substate'] = self.next_state_if_valid_data
                reply_message = self.next_message_if_valid_data
            else:
                return_dict['substate'] = self.next_state_if_invalid_data
                reply_message = self.next_message_if_invalid_data
        
        return return_dict, reply_message