# development only !!!!!!
# for testint line sdk

from linebot import(
    LineBotApi, WebhookHandler
)
from config import line_bot_config
li = LineBotApi(line_bot_config["CHANNEL_ACCESS_TOKEN"])

#14104899943631