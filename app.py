from flask import Flask, jsonify
from flask_restful import Api

from db import db

import models
from resources.store import StoreResource, StoreResourceAll



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1213456789-pst-api@localhost:3307/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)
api.add_resource(StoreResourceAll, "/stores")
api.add_resource(StoreResource, "/stores/<int:store_id>")
# api.add_resource(StoreResource, "/stores", "method=['POST']")

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)



