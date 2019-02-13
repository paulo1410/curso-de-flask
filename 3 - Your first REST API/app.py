from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
stores = [{
    'name': 'My Store',
    'items': [{'name': 'my item', 'price': 15.99}]
}]


@app.route('/')
def home():
    return render_template('index.html')


# GET /store
@app.route('/store/')
def get_stores():
    return jsonify({'stores': stores})  # Converte stores que é uma lista para o formato json


# post /store data: {name :}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()  # Converte Json string em um dicionário Python
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    # Sem jsonify ele falharia ao tentar retornar um dicionário pq é preciso retornar uma string
    return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over get_stores
    for store in stores:
        if store['name'] == name:  # Store é uma lista, name é um dicinário
            return jsonify(store)
    return jsonify({'message': 'Store não encontrado'})


# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price'],
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store não encontrado'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'Store não encontrado'})


app.run(port=5000)
