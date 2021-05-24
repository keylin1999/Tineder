from typing import Tuple

import sqlalchemy

class StatusMessageSetting:

    substate_name = "status_message_setting"
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
               session) -> Tuple[dict, str]:
        
        return_dict = {}


        if message['type'] == 'text':
            message = message['content']
            if message == 'n':
                return_dict['substate'] = self.next_state_if_default
                reply_message = self.next_message_if_default
            else:
                return_dict['status_message'] = message
                return_dict['substate'] = self.next_state_if_not_default
                reply_message = self.next_message_if_not_default % return_dict['status_message']

            return return_dict, reply_message