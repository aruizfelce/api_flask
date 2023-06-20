from flask import request, jsonify
from flask_restful import Resource, abort
from models.store import StoreModel
from db import db

class StoreResource(Resource):
    def get(self, store_id):
        return abort_if_store_doesnt_exist(store_id)
    
    def put(self, store_id):
        if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("name"):
            return {"message": "Debe suministrar el nombre"}, 400
        
        store = abort_if_store_doesnt_exist(store_id,False)
        store.name = request.get_json().get("name")

        db.session.add(store)
        db.session.commit()
        return {"message": "Store {} actualizado satisfactoriamente".format(store.id)}, 201
    
    def delete(self, store_id):
        store = abort_if_store_doesnt_exist(store_id,False)
        try:
            db.session.delete(store)
            db.session.commit()
        except:
            return {"message": "No se pudo eliminar la tienda"}, 500
        return {"message": "Store {} eliminado satisfactoriamente".format(store_id)}, 201

class StoreResourceAll(Resource):
    def get(self):
        stores = StoreModel.query.all()
        if stores:
            return [store_to_json(store) for store in stores], 200
            #return {"stores": [store_to_json(store) for store in store]}, 200
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
    
def store_to_json(store):
    return {
        "id": store.id,
        "name": store.name
    }

def abort_if_store_doesnt_exist(store_id, json=True):
    store = StoreModel.query.get(store_id)
    if store is None:
        abort(404, message="Tienda con el id {} no existe".format(store_id))
    if json:
        return store_to_json(store), 200
    return store
    #return {"store": store_to_json(store)}, 200
    