from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
# reqparse garante que apenas alguns elementos possam ser passados no payload
from security import autenticar, identificar

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, autenticar, identificar)  # jwt ficar um endpoint /auth

items = []


class Items(Resource):
    def get(self):
        return {'items': items}


class Item(Resource):  # Classe Item herda Resource (definição de recursos)
    parser = reqparse.RequestParser()
    # Como não há self. em frente a parser, então parser pertence a classe, não ao objeto.
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Este campo não pode ser deixado vazio')   # tudo que não for "price" será descartado.
    @jwt_required()  #  Metodos com esse decorator requer o token auteticado no header
    #  O header HTTP do server deve informar (juntamente com a resposta) Key: Authorization  Value: jwt <token>
    def get(self, name):  # Definição dos métidos get, post, etc
        # for item in items:
        #     if item['name'] == name:
        #         return item  # Não precis do jsonify no flask_restful
        item = next(filter(lambda x: x['name'] == name, items), None)
        # next retorna o primeiro item achado pela função filter. Se next não achar um item, retorna None
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):  # "is not None" está implícito
            return {'message': f'Um item o nome "{name}" já existe'}, 400  # 400 é bad request
        # data = request.get_json()  # Usado quando não havia reqparse
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201   # Status code HTPP "created"

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message:': f'Item {name} deletado'}

    def put(self, name):
        # data = request.get_json()  --> todos os json no body serão repassados ao data
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)  # Parser garante que somente o price será alterado.
        return {'item': item}



api.add_resource(Item, '/item/<string:name>')  # Definição dos endpoint dos recursos
api.add_resource(Items, '/items')


app.run(port=5000, debug=True)
