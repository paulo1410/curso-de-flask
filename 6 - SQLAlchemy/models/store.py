
from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'  # informa ao SQLAlchemy o nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  #  Busca a chave estrangeira em ItemModel e o associa a uma lista
    # Pode haver vários items em um store
    # lazy dynamic informa que não criar um objeto para cada item no store automaticamente.
    # com lazy dynamic, toda vez que chama o json, ele terá que consultar o banco

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):  # serve tanto pra inserir, quanto update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
