from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        return items
        connection.close()

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Este campo não pode ser deixado vazio')

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE namedb=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close
        if row:
            return {'item': {"name": row[0], 'price': row[1]}}

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self, name):
        item = Item.find_by_name(name)
        if item:
            return {'message': f'Um item {name} já existe'}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            Item.insert(item)
        except:
            return {'message': 'Ocorreu um erro tentando gravar no banco'}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = ("INSERT INTO items VALUES (?, ?)")
        cursor.execute(insert_query, (item['name'], item['price']))
        connection.commit()
        connection.close()


    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            delete_query = ("DELETE FROM items WHERE namedb=?")
            cursor.execute(delete_query, (name,))
            connection.commit()
            connection.close()
            return {'message': f'item {name} apagado com sucesso'}
        return {'message': f'item {name} não existe'}


    def put(self, name):
        item = Item.find_by_name(name)
        data = Item.parser.parse_args()
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message': 'Ocorreu um erro tentando criar um item no banco'}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {'message': 'Ocorreu um erro tentando atualizar o item'}, 500
        return updated_item

    @staticmethod
    def update(item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = ("UPDATE items SET pricedb=? WHERE namedb=?")
        cursor.execute(update_query, (item['price'], item['name']))
        connection.commit()
        connection.close()
