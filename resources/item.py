from flask import request, jsonify
from flask_restful import Resource, abort
from models.items import ItemModel
from db import db
from resources.store import StoreResource
from datetime import datetime,date
from tools.tools import Tools

class ItemResource(Resource):
    def get(self, item_id):
        return abort_if_item_doesnt_exist(item_id)
    
    def put(self, item_id):
        if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("name"):
            return {"message": "Debe suministrar el nombre"}, 400
        
        if not request.get_json().get("price"):
            return {"message": "Debe suministrar el precio"}, 400
        
        item = abort_if_item_doesnt_exist(item_id,False)

        item.name = request.get_json().get("name")
        item.price = request.get_json().get("price")

        db.session.add(item)
        db.session.commit()
        return {"message": "Item {} actualizado satisfactoriamente".format(item.id)}, 201
    
    def delete(self, item_id):
        item = abort_if_item_doesnt_exist(item_id,False)
        try:
            db.session.delete(item)
            db.session.commit()
        except:
            return {"message": "No se pudo eliminar el item"}, 500
        return {"message": "Item {} eliminado satisfactoriamente".format(item_id)}, 201
    
class ItemAllResource(Resource):
    def get(self):
        items = ItemModel.query.all()
        if items:
            return [Tools.convertir_json_sql(item) for item in items], 200
            #return {"items": [Tools.convertir_json_sql(item) for item in items]}, 200
        return {"mensaje": "No se encontraron items"}, 404
    
    def post(self):
        if not request.get_json().get("store_id"):
            return {"message": "Debe suministrar el id de la tienda"}, 400
        
        if StoreResource.get(self, request.get_json().get("store_id")) == 404:
            return {"mensaje": "No se encontró la tienda"}, 404
        
        if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("name"):
            return {"message": "Debe suministrar el nombre"}, 400
        
        if not request.get_json().get("price"):
            return {"message": "Debe suministrar el precio"}, 400
        
        new_item = ItemModel(**request.get_json())

        db.session.add(new_item)
        db.session.commit()
        return {"message": "Item creado satisfactoriamente"}, 201
    
class ItemByStoreResource(Resource):
    def get(self, store_id):
        if StoreResource.get(self, store_id) == 404:
            return {"mensaje": "No se encontró la tienda"}, 404
        
        items = ItemModel.query.filter_by(store_id=store_id).all()
        
        if items:
            return [Tools.convertir_json_sql(item) for item in items], 200
            #return {"items": [Tools.convertir_json_sql(item) for item in items]}, 200
        return {"mensaje": "No se encontraron items"}, 404
    
def abort_if_item_doesnt_exist(item_id, json=True):
    item = ItemModel.query.get(item_id)
    if item is None:
        abort(404, message="Item con el id {} no existe".format(item_id))
    if json:
        return Tools.convertir_json_sql(item)
    return item

