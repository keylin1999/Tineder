# 
from linebot import(
    LineBotApi
)
from config import line_bot_config
line_bot_api = LineBotApi(line_bot_config["CHANNEL_ACCESS_TOKEN"])