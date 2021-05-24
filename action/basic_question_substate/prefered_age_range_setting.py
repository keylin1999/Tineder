from model.user import User
from typing import Tuple

import sqlalchemy
import re

pattern = re.compile("^[1-9]{0,1}[0-9]{1}~[1-9]{0,1}[0-9]{1}$")

class PreferedAgeSetting:
    
    substate_name = "prefered_age_range_setting"
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
            if len(message) > 5:
                match = False
            else:    
                search = pattern.search(message)
                if search is None:
                    match = False
                else:
                    start, end = message.split("~")
                    start = int(start)
                    end = int(end)
                    if start <= end:
                        match = True
                    else:
                        match = False

            if match:
                user = session.query(User).filter_by(id=user_id).first()
                user.prefered_age_range_start = start
                user.prefered_age_range_end = end
                session.commit()
                return_dict['substate'] = self.next_state_if_valid_data
                reply_message = self.next_message_if_valid_data
            else:
                return_dict['substate'] = self.next_state_if_invalid_data
                reply_message = self.next_message_if_invalid_data

        return return_dict, reply_message
            