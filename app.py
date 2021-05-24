import pprint
from flask import Flask, request, abort
from flask import send_file
from linebot.models.messages import ImageMessage
from linebot.models.send_messages import ImageSendMessage
from config import line_bot_config, app_load_config, bot_name, user_picture_dir, chatroom_picture_dir, domain_rl
from model import db
from model.user import User
from sqlalchemy import func
from util.get_image import get_image, get_image_content, get_image_chat_content
from state_store.dictionary import Dictionary_State_Store
from action.unpair_request import unpair_user
from action import(
    basic_questions,
    # chat_setting,
    pair_request,
    unpair_request,
    # user_config_setting
)

from linebot import(
    LineBotApi, WebhookHandler
)


from linebot.exceptions import(
    InvalidSignatureError
)

from linebot.models import(
    MessageEvent,
    FollowEvent,
    UnfollowEvent,
    TextMessage,
    TextSendMessage
)

line_bot_api = LineBotApi(line_bot_config["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(line_bot_config["CHANNEL_SECRET"])

app = Flask(__name__)
app_load_config(app)
db.app = app
db.init_app(app)
db.create_all()

state_store = Dictionary_State_Store()

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@app.route('/image/<img_name>')
def get_profile_image(img_name):
    img_path = user_picture_dir + '/' + img_name
    return send_file(img_path, mimetype='image/jpeg')

@app.route('/chat_img/<img_name>')
def get_chat_image(img_name):
    img_path = chatroom_picture_dir + '/' + img_name
    return send_file(img_path, mimetype='image/jpeg')

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    message = event.message.text
    user_id = event.source.user_id
    
    if message[:len(bot_name) + 1] == bot_name + " ":
        command = message[len(bot_name) + 1:]
        if command == "":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Hi, I'm HJack. What can I help for you")
            )
        elif command == basic_questions.session_name:
            state_store.add_state(user_id=user_id)
            state = {}
            message = {
                "type":"text",
                "content":""
            }
            return_dict, return_message, finished = basic_questions.basic_question(user_state=state,
                                                                                   user_id=user_id,
                                                                                   message=message,
                                                                                   session=db.session)
            state = return_dict
            state['session'] = basic_questions.session_name
            state_store.update_state(user_id=user_id,
                                     dictionary=state)
            
        elif command == pair_request.session_name:
            state = {}
            message = {
                "type":"text",
                "content":""
            }
            return_dict, return_message, finished = pair_request.pair_request(user_state=state,
                                                                                   user_id=user_id,
                                                                                   message=message,
                                                                                   session=db.session)
            state_store.del_state(user_id=user_id)

        elif command == unpair_request.session_name:
            state = {}
            message = {
                "type":"text",
                "content":""
            }
            return_dict, return_message, finished = unpair_request.unpair_request(user_state=state,
                                                                                   user_id=user_id,
                                                                                   message=message,
                                                                                   session=db.session)
            state_store.del_state(user_id=user_id)
        
        if return_message is not None:
            line_bot_api.reply_message(
                    event.reply_token,
                    return_message
            )
    else:
        ex = state_store.user_id_exist(user_id=user_id)
        if ex:
            # TODO if in session, add a prefix to every message answer by bot
            state = state_store.get_state(user_id=user_id)
            # print(state_store.store)
            if state['session'] == basic_questions.session_name:
                message = {
                    "type":"text",
                    "content":event.message.text
                }
                return_dict, return_message, finished = basic_questions.basic_question(user_state=state,
                                                                                       user_id=user_id,
                                                                                       message=message,
                                                                                       session=db.session)
                if finished:
                    state_store.del_state(user_id=user_id)
                else:
                    return_dict['session'] = basic_questions.session_name
                    state_store.update_state(user_id=user_id,
                                             dictionary=return_dict)
                line_bot_api.reply_message(
                    event.reply_token,
                    return_message
                )
            
        else:
            user = db.session.query(User).filter_by(id=user_id).first()
            if user.paired_id is not None:
                # TODO use reply_message as much as possible
                line_bot_api.push_message(
                    user.paired_id,
                    TextSendMessage(text=event.message.text)
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="你目前還沒有配對對象喔～")
                )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    content_id = event.message.id
    user_id = event.source.user_id

    ex = state_store.user_id_exist(user_id=user_id)
    if ex:
        state = state_store.get_state(user_id=user_id)
        if state['session'] == basic_questions.session_name:
            message = {
                "type":"image_id",
                "content":content_id
            }
            return_dict, return_message, finished = basic_questions.basic_question(user_state=state,
                                                                                        user_id=user_id,
                                                                                        message=message,
                                                                                        session=db.session)
            if finished:
                state_store.del_state(user_id=user_id)
            else:
                return_dict['session'] = basic_questions.session_name
                state_store.update_state(user_id=user_id,
                                            dictionary=return_dict)
            line_bot_api.reply_message(
                event.reply_token,
                return_message
            )
        else:
            pass
    else:
        # user send image to it's paired user
        # TODO maybe blocked if chat blocks image sending 
        user = db.session.query(User).filter_by(id=user_id).first()
        if user.paired_id is not None:
            response = line_bot_api.get_message_content(content_id)
            get_image_chat_content(response.content, content_id)
            line_bot_api.push_message(
                user.paired_id,
                ImageSendMessage(
                    original_content_url=domain_rl + '/chat_img/' + str(content_id) + '.jpg',
                    preview_image_url=domain_rl + '/chat_img/' + str(content_id) + '.preview.jpg'
                )
            )
            print(domain_rl + '/chat_img/' + str(content_id) + '.jpg')
        else:
            # user don't have pair and is not in session state
            pass
            




@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    picture_id = None
    status_message = profile.status_message
    name       = profile.display_name
    language   = profile.language
    activate   = 1
    paired_id  = None

    user = db.session.query(User).filter_by(id=user_id).first()
    if user is not None:
    # change the value activate from 0 to 1
        user.activate = 1
    else:
    # add new user row into user table
        max_pic_id = db.session.query(func.max(User.picture_id)).scalar()
        if max_pic_id == None:
        # if there is no user at the user table
            max_pic_id = 0
        picture_id = max_pic_id + 1 # TODO change to uuid or random big number and make sure there's no repeat
        get_image(url=profile.picture_url, id=picture_id)

        new_user = User(user_id=user_id,
                        name=name,
                        picture_id=picture_id,
                        status_message=status_message,
                        language=language,
                        activate=activate,
                        paired_id=paired_id)

        db.session.add(new_user)

    db.session.commit()
    

@handler.add(UnfollowEvent)
def handle_unfollow(event):

    # update the value activate from 1 to 0
    # unpaired the one that is paired against it
    # send message to the one that is unpaired

    user_id = event.source.user_id
    user = db.session.query(User).filter_by(id=user_id).first()

    if user is not None:
        user.activate = 0
        paired_id = user.paired_id
        
        unpair_user(user_id, paired_id, db.session)





if __name__ == '__main__':
    app.run(port= 3003, debug=True)

