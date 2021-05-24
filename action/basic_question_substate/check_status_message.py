from model.user import User
from typing import Tuple

import sqlalchemy

class CheckStatusMessage:

    substate_name = "check_status_message"
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
               session: sqlalchemy.orm.Session) -> Tuple[dict, str]:
        
        return_dict = {}

        # TODO save status message to the database

        if message['type'] == 'text':
            message = message['content']
            if message == 'n':
                return_dict['substate'] = self.next_state_if_not_confirm
                reply_message = self.next_message_if_not_confirm % user_state['status_message']
            else:
                user = session.query(User).filter_by(id=user_id).first()
                user.status_message = user_state['status_message']
                session.commit()
                return_dict['substate'] = self.next_state_if_confirm
                reply_message = self.next_message_if_confirm

        return return_dict, reply_message