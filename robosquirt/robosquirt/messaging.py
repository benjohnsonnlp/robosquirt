import fbchat

from robosquirt.robosquirt.config import config

settings_username = config.get('facebook', 'username')
settings_password = config.get('facebook', 'password')

def message_user(recipient, message, username=settings_username, password=settings_password):
    client = fbchat.Client(username, password)

    natalie = client.searchForUsers(name=recipient)[0]

    client.send(fbchat.Message(text=message), thread_id=natalie.uid)
