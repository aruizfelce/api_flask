from flask import request
from flask_restful import Resource
from models.store import StoreModel
from db import db
from tools.tools import Tools
from flask_jwt_extended import jwt_required
from schemas import StoreSchema
from marshmallow import ValidationError

class StoreResource(Resource):
    @jwt_required()
    def get(self, store_id):
        stores = StoreModel.query.get(store_id)
        if stores:
            store_schema = StoreSchema()
            return store_schema.dump(stores)
        return {"message": "Tienda {} no existe".format(store_id)}, 404
        #return Tools.abort_if_doesnt_exist(StoreModel,store_id)
    
    @jwt_required()
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
    
    @jwt_required()
    def delete(self, store_id):
        store = Tools.abort_if_doesnt_exist(StoreModel,store_id,False)
        try:
            db.session.delete(store)
            db.session.commit()
        except:
            return {"message": "No se pudo eliminar la tienda"}, 500
        
        return {"message": "Store {} eliminado satisfactoriamente".format(store_id)}, 201

class StoreAllResource(Resource):
    @jwt_required()
    def get(self):
        stores = StoreModel.query.all()
        stores_schema = StoreSchema(many=True)
        if stores:
            return stores_schema.dump(stores)
       #if stores:
        #    return [Tools.convertir_json_sql(store) for store in stores], 200
        #return {"mensaje": "No se encontraron tiendas"}, 404 """
    
    @jwt_required()
    def post(self):
        json_data = request.get_json()
        store_schema = StoreSchema()
        if not json_data:
            return {"message": "No se envió la data"}, 400
        try:
            data = store_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
    
        store = StoreModel(**data)
        db.session.add(store)
        db.session.commit()
        return {"message": "Store creada satisfactoriamente"}, 201
    
        """ if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("name"):
            return {"message": "Debe suministrar el nombre"}, 400
        
        new_store = StoreModel(**request.get_json())

        db.session.add(new_store)
        db.session.commit()
        return {"message": "Store creada satisfactoriamente"}, 201 """
    
class StorebyNameResource(Resource):
    # @jwt_required()
    def get(self, name):
        store = StoreModel.query.filter_by(name=name).first() 
            
        if store:
            store_schema = StoreSchema()
            return store_schema.dump(store)
            #return Tools.convertir_json_sql(store), 200
        return {"mensaje": "No se encontró la tienda"}, 404