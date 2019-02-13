import sqlite3
from flask_restful import Resource, reqparse


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # username tem que estar no formato tuple
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,))  # username tem que estar no formato tuple
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user


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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message': 'Usuário já existe'}, 400


        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'Ususário criado com sucesso'}, 201
