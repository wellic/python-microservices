from dataclasses import dataclass

import requests
from flask import abort, Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish
from settings import ADMIN_URL, DB_HOST_NAME

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:root@{DB_HOST_NAME}/main'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title: str = db.Column(db.String(200))
    image: str = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='user_product_unique'),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer)
    product_id: int = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get(f'{ADMIN_URL}/api/user')
    json = req.json()

    user_id = None
    try:
        user_id = json['id']
        productUser = ProductUser(user_id=user_id, product_id=id)
        db.session.add(productUser)
        db.session.commit()

        #event
        publish('product_linked', id)
    except Exception as e:
        abort(400, f'You already liked this product pid={id} uid={user_id}')

    return jsonify({
        'message': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
