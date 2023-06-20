from flask import request, jsonify
from flask_restful import Resource
from models.store import StoreModel
from db import db
from tools.tools import Tools

class StoreResource(Resource):
    def get(self, store_id):
        return Tools.abort_if_doesnt_exist(StoreModel,store_id)
    
    def put(self, store_id):
        if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("name"):
            return {"message": "Debe suministrar el nombre"}, 400
        
        store = Tools.abort_if_doesnt_exist(StoreModel,store_id,False)

        store.name = request.get_json().get("name")

        db.session.add(store)
        db.session.commit()
        return {"message": "Store {} actualizado satisfactoriamente".format(store.id)}, 201
    
    def delete(self, store_id):
        store = Tools.abort_if_doesnt_exist(StoreModel,store_id,False)
        try:
            db.session.delete(store)
            db.session.commit()
        except:
            return {"message": "No se pudo eliminar la tienda"}, 500
        
        return {"message": "Store {} eliminado satisfactoriamente".format(store_id)}, 201

class StoreAllResource(Resource):
    def get(self):
        stores = StoreModel.query.all()
        if stores:
            return [Tools.convertir_json_sql(store) for store in stores], 200
            #return {"stores": [Tools.convertir_json_sql(store) for store in store]}, 200
        return {"mensaje": "No se encontraron tiendas"}, 404
    
    def post(self):
        if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("name"):
            return {"message": "Debe suministrar el nombre"}, 400
        
        new_store = StoreModel(**request.get_json())

        db.session.add(new_store)
        db.session.commit()
        return {"message": "Store creada satisfactoriamente"}, 201