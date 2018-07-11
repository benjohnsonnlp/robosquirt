import fbchat

from config import config

settings_username = config.get('facebook', 'username')
settings_password = config.get('facebook', 'password')


def message_user(recipient, message, username=settings_username, password=settings_password):
    client = fbchat.Client(username, password)

    recipient_user = client.searchForUsers(name=recipient)[0]

    client.send(fbchat.Message(text=message), thread_id=recipient_user.uid)


if __name__ == '__main__':
    message_user('ben johnson', 'test')
