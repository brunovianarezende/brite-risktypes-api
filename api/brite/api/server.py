import os

from sqlalchemy import create_engine
from flask import Flask, make_response, json

from brite.model.service import DbService

app = Flask(__name__)

def _make_json_response(obj, status=200):
    response = make_response(json.dumps(obj), status)
    response.headers["Content-Type"] = 'application/json; charset=utf-8'
    return response

def _db():
    if 'BACKEND' not in app.config:
        db_path = os.environ['SQLITE_PATH']
        engine = create_engine('sqlite:///%s' % db_path)
        app.config['BACKEND'] = DbService(engine)
    return app.config['BACKEND']

@app.route('/search/types/', methods=['GET'])
def search_types():
    db_service = _db()
    objects = db_service.get_types(order_by_name=True)
    return _make_json_response({'total': len(objects), 'types': objects})

def make_404_error(obj_id):
    response = {'error': "'%s' not found" % obj_id}
    return _make_json_response(response, 404)

@app.route('/types/<type_id>/', methods=['GET'])
def get_type(type_id):
    if not type_id.isdigit():
        return make_404_error(type_id)
    type_id = int(type_id)
    db_service = _db()
    result = db_service.get_type(type_id)
    if result is not None:
        return _make_json_response(result)
    else:
        return make_404_error(type_id)
