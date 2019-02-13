from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Este campo não pode ser deixado vazio')
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Todo item precisa de um store')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Um item {name} já existe'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)  # **data = data['price'], data['store_id']
        try:
            item.save_to_db()
        except:
            return {'message': 'Ocorreu um erro tentando gravar no banco'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'item {name} apagado com sucesso'}
        return {'message': f'item {name} não existe'}

    def put(self, name):
        item = ItemModel.find_by_name(name)
        data = Item.parser.parse_args()
        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {'message': 'Ocorreu um erro tentando criar um item no banco'}, 500
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()
