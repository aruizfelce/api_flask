from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

import models
from resources.store import StoreResource, StoreAllResource
from resources.item import ItemResource, ItemAllResource, ItemByStoreResource


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1213456789-pst-api@localhost:3307/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

db.init_app(app)
api = Api(app)
api.add_resource(StoreAllResource, "/stores")
api.add_resource(StoreResource, "/stores/<int:store_id>")

api.add_resource(ItemResource, "/items/<int:item_id>")
api.add_resource(ItemAllResource, "/items")
api.add_resource(ItemByStoreResource, "/items/store/<int:store_id>")

jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)



