from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from flask_migrate import Migrate
import models
from resources.store import StoreResource, StoreAllResource
from resources.item import ItemResource, ItemAllResource, ItemByStoreResource
from resources.user import UserResource, LoginResource, TokenRefresh

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1213456789-pst-api@localhost:3307/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

api.add_resource(StoreAllResource, "/stores")
api.add_resource(StoreResource, "/stores/<int:store_id>")

api.add_resource(ItemResource, "/items/<int:item_id>")
api.add_resource(ItemAllResource, "/items")
api.add_resource(ItemByStoreResource, "/items/store/<int:store_id>")

api.add_resource(UserResource, "/users/register")
api.add_resource(LoginResource, "/login")
api.add_resource(TokenRefresh, "/refresh")

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "El token está expirado.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Token inválido", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Debe suministrar el access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})

""" with app.app_context():
    db.create_all() """

if __name__ == "__main__":
    app.run(debug=True)



