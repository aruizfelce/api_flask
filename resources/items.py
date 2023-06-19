from flask import request, jsonify
from flask_restful import Resource
from models.items import ItemModel

class Item(Resource):
    def get(self):
        items = ItemModel.query.all()
        if items:
            return {"items": [self.item_to_json(item) for item in items]}, 200
           
        return {"message": "Items not found"}, 404
    
    def item_to_json(self, item):
        return {
            "id": item.id,
            "name": item.name,
            "price": item.price
        }