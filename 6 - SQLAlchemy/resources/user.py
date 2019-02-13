from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Este campo não pode ser deixado vazio')
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Este campo não pode ser deixado vazio')

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'Usuário já existe'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'Ususário criado com sucesso'}, 201
