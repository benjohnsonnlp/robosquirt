import fbchat


def message_user(recipient, message):
    username = 'username'
    password = 'replace'
    client = fbchat.Client(username, password)

    natalie = client.searchForUsers(name=recipient)[0]

    client.send(fbchat.Message(text=message), thread_id=natalie.uid)
