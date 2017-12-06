from flask import Flask, make_response, json

app = Flask(__name__)

_db = lambda: app.config['BACKEND']

@app.route('/search/types/', methods=['GET'])
def search_types():
    db_service = _db()
    objects = db_service.get_types(order_by_name=True)
    return make_response(json.dumps({'total': len(objects), 'types': objects}))

def make_404_error(obj_id):
    response = {'error': "'%s' not found" % obj_id}
    return make_response(json.dumps(response), 404)

@app.route('/types/<type_id>/', methods=['GET'])
def get_type(type_id):
    if not type_id.isdigit():
        return make_404_error(type_id)
    type_id = int(type_id)
    db_service = _db()
    result = db_service.get_type(type_id)
    if result is not None:
        return make_response(json.dumps(result))
    else:
        return make_404_error(type_id)
