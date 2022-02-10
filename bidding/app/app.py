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

@app.route('/bidding/hello')
def hello():
    return 'Hello, welcome to the ESBay Bidding API\n'
@app.route('/api/bidding/create', methods=['POST', 'GET'])
def post_create():
    product_id = None
    user_id = None
    price = None
    if request.method == 'POST':
        product_id = request.form['product_id']
        user_id = request.form['user_id']
        price = request.form['price']

    item = models.Bidding()
    item.product_id = product_id
    item.user_id = user_id
    item.price = price

    models.db.session.add(item)
    models.db.session.commit()

    response = jsonify({'message': 'Bidding added', 'bidding': item.to_json()})

    return response
#
@app.route('/api/bidding', methods=['GET'])
def products():
    data = []
    for row in models.Bidding.query.all():
        data.append(row.to_json())
    response = jsonify({ 'results': data })
    return response

@app.route('/api/bidding/byprice', methods=['POST'])
def byprice():
    data = []

    product_id = request.form['product_id']

    bidding = models.Bidding.query
    bidding_filter = bidding.filter(models.Bidding.product_id == product_id)
    bidding = bidding_filter.order_by(models.Bidding.price.desc()).all()
    for row in bidding:
        data.append(row.to_json())
    response = jsonify({ 'max_price': data[0]['price']})
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

