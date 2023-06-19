from flask import request, jsonify
from flask_restful import Resource, abort
from models.store import StoreModel

class StoreResource(Resource):
    def get(self):
        store = StoreModel.query.all()
        if store:
            return {"stores": [self.store_to_json(store) for store in store]}, 200
           
        return {"message": "Store not found"}, 404
    
    def get(self, store_id):
        return self.abort_if_store_doesnt_exist(store_id)
    
    """ def post(self):
        return {"message": "Store created successfully."}, 201
        store = StoreModel(**request.get_json())
        store.save_to_db()
        return {"message": "Store created successfully."}, 201 """
    
    def store_to_json(self, store):
        return {
            "id": store.id,
            "name": store.name
        }
    
    def abort_if_store_doesnt_exist(self, store_id):
        store = StoreModel.find_by_id(store_id)
        if store is None:
            abort(404, message="Store {} doesn't exist".format(store_id))
        return {"store": self.store_to_json(store)}, 200
    