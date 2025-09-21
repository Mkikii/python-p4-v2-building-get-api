#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood, desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = [bakery_dict.to_dict() for bakery_dict in Bakery.query.all()]
    return make_response(jsonify(all_bakeries), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    resp = bakery.to_dict()
    return make_response(resp, 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    
    baked_goods = [goods.to_dict() for goods in BakedGood.query.order_by(desc(BakedGood.price)).all()]
    return make_response(jsonify(baked_goods), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():

    most_expensive_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    return make_response(jsonify(most_expensive_good.to_dict()), 200)
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)