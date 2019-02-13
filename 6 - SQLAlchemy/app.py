from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import autenticar, identificar
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  #  Para operar sqlalchemy com qq outro banco, basta mudar essa linha
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # desabilita o track do flask, uma vez que o alchemy possui seu próprio track
app.secret_key = "jose"
api = Api(app)
jwt = JWT(app, autenticar, identificar)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores/')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
