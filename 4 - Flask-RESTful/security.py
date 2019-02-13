from user import User

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def autenticar(username, password):
    user = username_table.get(username, None)  # get é uma função do dicionário
    if user and user.password == password:
        return user


def identificar(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
