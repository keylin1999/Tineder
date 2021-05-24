from typing import Tuple

import sqlalchemy
from model.user import User
from util.get_line_bot_api import line_bot_api
from config import domain_rl

from linebot.models import(
    ImageSendMessage
)

class CheckName:

    substate_name = "check_name"
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

        # TODO write name to the database

        if message['type'] == 'text':
            message = message['content']
            if message == 'n':
                return_dict['substate'] = self.next_state_if_not_confirm
                reply_message = self.next_message_if_not_confirm % user_state['name']
            else:
                user = session.query(User).filter_by(id=user_id).first()
                user.name = user_state['name']
                session.commit()
                user = session.query(User).filter_by(id=user_id).first()
                im = ImageSendMessage(original_content_url=domain_rl + '/image/' + str(user.picture_id) + '.jpg',
                                    preview_image_url=domain_rl + '/image/' + str(user.picture_id) + '.preview.jpg')
                line_bot_api.push_message(user_id, im)

                return_dict['substate'] = self.next_state_if_confirm
                reply_message = self.next_message_if_confirm

            return return_dict, reply_message