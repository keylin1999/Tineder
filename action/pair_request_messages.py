message = {
    "en":{
        "pair_fail": "Sorry there are no available candidate",
        "pair_success": "Paired Success! Enjoy your talk",
        "sent_to_paired": "You're paired! Enjoy your talk"
    },
    "zh":{
        "pair_fail": "Sorry there are no available candidate",
        "pair_success": "Paired Success! Enjoy your talk",
        "sent_to_paired": "You're paired! Enjoy your talk"
    }
}
EN = 'en'
ZH = 'zh'

def get_message(state, language='en'):
    return message['en'][state]
