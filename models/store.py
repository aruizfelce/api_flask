from db import db
from models.item import ItemModel

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship(ItemModel, backref="storemodel", lazy=True, cascade="all, delete")