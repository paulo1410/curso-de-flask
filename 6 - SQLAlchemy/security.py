from models.user import UserModel


def autenticar(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identificar(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
