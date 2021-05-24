line_bot_config = {
    "CHANNEL_ACCESS_TOKEN" : "",
    "CHANNEL_SECRET" : ""
}

domain_rl = ""

mysql_url = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8mb4".format(
    drivername="mysql+pymysql",
    user="root",
    passwd="root",
    host="localhost",
    port="3306",
    db_name="chatbot"
)

user_picture_dir = "user_picture"
chatroom_picture_dir = "chat_picture"

bot_name = "HJack"

def app_load_config(app):
    """ The funciton automatically loads the config define in this file to the app 
    
    Args:
        app (Flask app)
    """
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url