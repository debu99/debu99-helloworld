import json, os
from flask import request

def configure_routes(app):
    @app.route('/')
    def index():
        return '<h1>Hello World from</h1> ' + os.uname()[1] 

    @app.route('/healthz')
    def healthcheck():
        return '200OK'

    @app.route('/hello', methods=['GET', 'POST'])
    def foo():
        if request.method != 'POST':
            return 'Please post data'
        else:
            data = request.get_json()
            return 'curl -i -XPOST -H "Content-Type: application/json" -d \'' + json.dumps(data) + '\' ' + request.url + '\n\n' + json.dumps(data)

    @app.route('/post', methods=['POST'])
    def post():
        headers = request.headers
        auth_token = headers.get('authorization-sha256')
        if not auth_token:
            return 'Unauthorized', 401

        data_string = request.get_data()
        data = json.loads(data_string)

        request_id = data.get('request_id')
        payload = data.get('payload')

        if request_id and payload:
            return 'Ok', 200
        else:
            return 'Bad Request', 400
