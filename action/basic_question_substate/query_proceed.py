from typing import Tuple

import sqlalchemy
from model.user import User

class QueryProceed:

    substate_name = "query_proceed"
    next_state_if_proceed = ""
    next_message_if_proceed = ""
    next_state_if_not_proceed = ""
    next_message_if_not_proceed = ""
    next_state_if_invalid_data = ""
    next_message_if_invalid_data = ""

    def __init__(self,
                 next_state_if_proceed,
                 next_message_if_proceed,
                 next_state_if_not_proceed,
                 next_message_if_not_proceed,
                 next_state_if_invalid_data,
                 next_message_if_invalid_data) -> None:
        
        self.next_state_if_proceed = next_state_if_proceed
        self.next_message_if_proceed = next_message_if_proceed
        self.next_state_if_not_proceed = next_state_if_not_proceed
        self.next_message_if_not_proceed = next_message_if_not_proceed
        self.next_state_if_invalid_data = next_state_if_invalid_data
        self.next_message_if_invalid_data = next_message_if_invalid_data
        
    def action(self,
               user_state: dict,
               user_id:str,
               message: dict,
               session:sqlalchemy.orm.Session) -> Tuple[dict, str]:
        
        return_dict = {}

        if message['type'] == 'text':
            message = message['content']
            if message == 'Y':
                return_dict['substate'] = self.next_state_if_proceed
                user = session.query(User).filter_by(id=user_id).first()
                name = user.name
                reply_message = self.next_message_if_proceed % name
            elif message == 'n':
                return_dict['substate'] = self.next_state_if_not_proceed
                reply_message = self.next_message_if_not_proceed
            else:
                return_dict['substate'] = self.next_state_if_invalid_data
                reply_message = self.next_message_if_invalid_data

        return return_dict, reply_message