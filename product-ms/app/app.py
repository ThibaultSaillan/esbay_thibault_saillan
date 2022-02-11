from flask import Flask, make_response, request, json, jsonify
import models

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY = "This is an INSECURE secret!! DO NOT use this in production!",
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@database/esbay',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
))

models.init_app(app)
models.create_table(app)

@app.route('/products/hello')
def hello():
    return 'Hello, welcome to the ESBay Product API\n'

@app.route('/api/product/create', methods=['POST', 'GET'])
def post_create():
    name = None
    seller = None
    price = None
    if request.method == 'POST':
        name = request.form['name']
        seller = request.form['seller']
        price = request.form['price']
    elif request.method == 'GET':
        name = request.args.get('name')
        seller = request.args.get('seller')
        price = request.args.get('price')

    item = models.Product()
    item.name = name
    item.seller = seller
    item.price = price

    models.db.session.add(item)
    models.db.session.commit()

    response = jsonify({'message': 'Product added', 'product': item.to_json()})

    return response



@app.route('/api/products', methods=['GET'])
def products():
    data = []

    for row in models.Product.query.all():
        data.append(row.to_json())
    response = jsonify({ 'results': data })
    return response

@app.route('/api/search', methods=['GET', 'POST'])
def search():
    name = request.form['name']
    products = []

    for row in models.Product.query.filter(models.Product.name.like('%' + name + '%')).all():
        products.append(row.to_json())
    response = jsonify({ 'results': products })
    return response

    products_query = models.Product.query
    products = products_query.filter(models.Product.name.like('%' + name + '%'))
    products = products.order_by(models.Product.name).all()
    products = products.to_json
    response = jsonify({ 'results': products })
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
