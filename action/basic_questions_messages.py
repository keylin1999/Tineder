entry_message = {
    "en" :{
        "query_proceed"                       : "We will walk throgh a series of setting to ensure that you are satisfied with your profile! Do you want to proceed? (Y/n)",
        "name_setting"                        : "Your name is now set as '%s' do you want to change? Changing it by typing strings other than 'n'.",
        "check_name"                          : "Are you sure to set your name as '%s' ? (Y/n)",
        "picture_setting"                     : "Your picture is now set as above do you want to change? Changing it by sending the new photo or type anything",
        "check_picture"                       : "Do you want to use this new picture as your profile photo? (Y/n)",
        "status_message_setting"              : "Your status message is now set as '%s' . Do you wnat to change? (type n to not change)",
        "check_status_message"                : "Are you sure to set your status message as '%s' ? (Y/n)",
        "gender_setting"                      : "What is your gender (male/female)",
        "age_setting"                         : "What is your age (value between 10 and 99)",
        "prefered_gender_setting"             : "Which gender do your pefered to talk (male/female)",
        "prefered_age_range_setting"          : "The prefered age range to talk to (like 10~30)",
        "finish"                              : "Setup finished",
        "declined"                            : "Setup declined",
        "invalid_Yn"                          : "Please enter 'Y' or 'n' which means yes and no",
        "invalid_gender"                      : "Please enter 'male' or 'female'",
        "invalid_age"                         : "Please enter age between 10~99",
        "invalid_age_range"                   : "Please enter agerange with format '10~30'"
    },
    "zh":{
        "query_proceed"                       : "We will walk throgh a series of setting to ensure that you are satisfied with your profile! Do you want to proceed? (Y/n)",
        "name_setting"                        : "Your name is now set as '%s' do you want to change? Changing it by typing strings other than 'n'.",
        "check_name"                          : "Are you sure to set your name as '%s' ? (Y/n)",
        "picture_setting"                     : "Your picture is now set as above do you want to change? Changing it by sending the new photo or type anything",
        "check_picture"                       : "Do you want to use this new picture as your profile photo? (Y/n)",
        "status_message_setting"              : "Your status message is now set as '%s' . Do you wnat to change? (type n to not change)",
        "check_status_message"                : "Are you sure to set your status message as '%s' ? (Y/n)",
        "gender_setting"                      : "What is your gender (male/female)",
        "age_setting"                         : "What is your age (value between 10 and 99)",
        "prefered_gender_setting"             : "Which gender do your pefered to talk (male/female)",
        "prefered_age_range_setting"          : "The prefered age range to talk to (like 10~30)",
        "finish"                              : "Setup finished",
        "declined"                            : "Setup declined",
        "invalid_Yn"                          : "Please enter 'Y' or 'n' which means yes and no",
        "invalid_gender"                      : "Please enter 'male' or 'female'",
        "invalid_age"                         : "Please enter age between 10~99",
        "invalid_age_range"                   : "Please enter agerange with format '10~30'"
    }
}
EN = 'en'
ZH = 'zh'

def get_entry_message(state, language='en'):
    return entry_message[language][state]
