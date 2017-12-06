from flask import Flask, make_response, json

app = Flask(__name__)

_db = lambda: app.config['BACKEND']

@app.route('/search/types/', methods=['GET'])
def search_types():
    db_service = _db()
    objects = db_service.get_types(order_by_name=True)
    return make_response(json.dumps({'total': len(objects), 'types': objects}))

@app.route('/types/<type_id>/', methods=['GET'])
def get_type(type_id):
    return make_response("I will return %s data" % type_id)
