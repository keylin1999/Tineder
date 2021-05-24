# action that starts when user start follow the bot
# the bot will walk through some basic information include
# gender, age, hobby(few menus for user to select)
# picture, status message and who do he/she wants to pair
# (show the default value and ask them whether to 
#  hide or modify them)

from typing import Tuple

session_name = "setup"
import sqlalchemy
from linebot.models import TextSendMessage

from action.basic_question_substate import *
from action.basic_questions_messages import get_entry_message

query_proceed_u = QueryProceed(
    next_state_if_proceed="name_setting",
    next_message_if_proceed=get_entry_message("name_setting"),
    next_state_if_not_proceed="declined",
    next_message_if_not_proceed=get_entry_message("declined"),
    next_state_if_invalid_data="query_proceed",
    next_message_if_invalid_data=get_entry_message("invalid_Yn")
)
name_setting_u = NameSetting(
    next_state_if_default="picture_setting",
    next_message_if_default=get_entry_message("picture_setting"),
    next_state_if_not_default="check_name",
    next_message_if_not_default=get_entry_message("check_name")
)
check_name_u = CheckName(
    next_state_if_confirm="picture_setting",
    next_message_if_confirm=get_entry_message("picture_setting"),
    next_state_if_not_confirm="name_setting",
    next_message_if_not_confirm=get_entry_message("name_setting")
)
picture_setting_u = PictureSetting(
    next_state_if_default="status_message_setting",
    next_message_if_default=get_entry_message("status_message_setting"),
    next_state_if_not_default="check_picture",
    next_message_if_not_default=get_entry_message("check_picture")
)
check_picture_u = CheckPicture(
    next_state_if_confirm="status_message_setting",
    next_message_if_confirm=get_entry_message("status_message_setting"),
    next_state_if_not_confirm="picture_setting",
    next_message_if_not_confirm=get_entry_message("picture_setting")
)
status_message_setting_u = StatusMessageSetting(
    next_state_if_default="gender_setting",
    next_message_if_default=get_entry_message("gender_setting"),
    next_state_if_not_default="check_status_message",
    next_message_if_not_default=get_entry_message("check_status_message")
)
check_status_message_u = CheckStatusMessage(
    next_state_if_confirm="gender_setting",
    next_message_if_confirm=get_entry_message("gender_setting"),
    next_state_if_not_confirm="status_message_setting",
    next_message_if_not_confirm=get_entry_message("status_message_setting")
)
gender_setting_u = GenderSetting(
    next_state_if_valid_data="age_setting",
    next_message_if_valid_data=get_entry_message("age_setting"),
    next_state_if_invalid_data="gender_setting",
    next_message_if_invalid_data=get_entry_message("invalid_gender")
)
age_setting_u = AgeSetting(
    next_state_if_valid_data="prefered_gender_setting",
    next_message_if_valid_data=get_entry_message("prefered_gender_setting"),
    next_state_if_invalid_data="age_setting",
    next_message_if_invalid_data=get_entry_message("invalid_age")
)
prefered_gender_setting_u = PreferedGenderSetting(
    next_state_if_valid_data="prefered_age_range_setting",
    next_message_if_valid_data=get_entry_message("prefered_age_range_setting"),
    next_state_if_invalid_data="prefered_gender_setting",
    next_message_if_invalid_data=get_entry_message("invalid_gender")
)
prefered_age_range_setting_u = PreferedAgeSetting(
    next_state_if_valid_data="finish",
    next_message_if_valid_data=get_entry_message("finish"),
    next_state_if_invalid_data="prefered_age_range_setting",
    next_message_if_invalid_data=get_entry_message("invalid_age_range")
)
substates = [query_proceed_u,
                 name_setting_u,
                 check_name_u,
                 picture_setting_u,
                 check_picture_u,
                 status_message_setting_u,
                 check_status_message_u,
                 gender_setting_u,
                 age_setting_u,
                 prefered_gender_setting_u,
                 prefered_age_range_setting_u]

def basic_question(user_state: dict, user_id:str, message: str, session:sqlalchemy.orm.Session) -> Tuple[dict, TextSendMessage, bool]:
    finished = False
    return_message = ""
    return_state = {}

    
    current_substate = user_state.pop("substate", None)

    # print("\n\n", current_substate, "\n\n")

    if current_substate == None:
        return_message = TextSendMessage(text=get_entry_message("query_proceed"))
        return_state = {'substate':'query_proceed'}
        finished = False

    else:
        for substate in substates:
            print(substate.substate_name, message)
            if current_substate == substate.substate_name:
                return_state, return_message = substate.action(
                    user_state=user_state,
                    user_id=user_id,
                    message=message,
                    session=session
                )
                return_message = TextSendMessage(text=return_message)
                print("jijij", return_message)
                break
    print(return_state, return_message, finished)

    if(return_state['substate'] == "finished" or
       return_state['substate'] == "declined"):
       finished = True
            
    return return_state, return_message, finished

