from flask import request, jsonify
from flask_restful import Resource, abort
from models.store import StoreModel

class StoreResource(Resource):
    def get(self, store_id):
        return abort_if_store_doesnt_exist(store_id)
    
    """ def post(self):
        return {"message": "Store created successfully."}, 201
        store = StoreModel(**request.get_json())
        store.save_to_db()
        return {"message": "Store created successfully."}, 201 """

class StoreResourceAll(Resource):
    def get(self):
        stores = StoreModel.query.all()
        if stores:
            return [store_to_json(store) for store in stores], 200
            #return {"stores": [store_to_json(store) for store in store]}, 200
        return {"mensaje": "No se encontraron tiendas"}, 404
    
    
def store_to_json(store):
    return {
        "id": store.id,
        "name": store.name
    }

def abort_if_store_doesnt_exist(store_id):
    store = StoreModel.query.get(store_id)
    if store is None:
        abort(404, message="Tienda con el id {} no existe".format(store_id))
    return store_to_json(store), 200
    #return {"store": store_to_json(store)}, 200
    