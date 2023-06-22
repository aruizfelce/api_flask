from flask import request
from flask_restful import Resource
from models import UserModel
from db import db
from tools.tools import Tools
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

class UserResource(Resource):
    def post(self):
        if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("username"):
            return {"message": "Debe suministrar el username"}, 400
        
        if not request.get_json().get("password"):
            return {"message": "Debe suministrar el password"}, 400
        
        if not request.get_json().get("rol"):
            return {"message": "Debe suministrar el rol"}, 400
        
        if UserModel.find_by_username(request.get_json().get("username")):
            return {"message": "Ya existe un usuario con ese username"}, 400
        
        new_user = UserModel(
            username=request.get_json().get("username"),
            rol=request.get_json().get("rol"),
            password=pbkdf2_sha256.hash(request.get_json().get("password")),
        )

        db.session.add(new_user)
        db.session.commit()
        return {"message": "Usuario creado satisfactoriamente"}, 201
    
class LoginResource(Resource):
    def post(self):
        if not request.get_json():
            return {"message": "No se envió la data"}, 400
        
        if not request.get_json().get("username"):
            return {"message": "Debe suministrar el username"}, 400
        
        if not request.get_json().get("password"):
            return {"message": "Debe suministrar el password"}, 400
        
        user = UserModel.find_by_username(request.get_json().get("username"))
        
        if user and pbkdf2_sha256.verify(request.get_json().get("password"), user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        return {"message": "Credenciales inválidas"}, 401

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200