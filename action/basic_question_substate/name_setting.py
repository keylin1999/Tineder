from typing import Tuple

import sqlalchemy
from model.user import User
from util.get_line_bot_api import line_bot_api
from config import domain_rl

from linebot.models import(
    ImageSendMessage
)

class NameSetting:

    substate_name = "name_setting"
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
        
        if message['type'] == 'text':
            message = message['content']
            if message == 'n':
                return_dict['substate'] = self.next_state_if_default
                reply_message = self.next_message_if_default
                user = session.query(User).filter_by(id=user_id).first()
                return_dict['name'] = user.name
                im = ImageSendMessage(original_content_url=domain_rl + '/image/' + str(user.picture_id) + '.jpg',
                                    preview_image_url=domain_rl + '/image/' + str(user.picture_id) + '.preview.jpg')
                line_bot_api.push_message(user_id, im)

            else:
                return_dict['substate'] = self.next_state_if_not_default
                return_dict['name'] = message
                reply_message = self.next_message_if_not_default % return_dict['name']

            return return_dict, reply_message

if __name__ == '__main__':
    im = ImageSendMessage(original_content_url=domain_rl + '/image/' + str(1) + '.jpg',
                          preview_image_url=domain_rl + '/image/' + str(1) + '.preview.jpg')
    print(domain_rl + '/image/' + str(1) + '.jpg')
    line_bot_api.push_message("Uaa379e85866bc38e672bbf641d77bc60",
                              im)
    