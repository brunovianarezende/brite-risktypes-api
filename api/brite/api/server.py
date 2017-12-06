from flask import Flask, make_response

app = Flask(__name__)

@app.route('/search/types/', methods=['GET'])
def search_types():
    return make_response("hi there")

@app.route('/types/<type_id>/', methods=['GET'])
def get_type(type_id):
    return make_response("I will return %s data" % type_id)
