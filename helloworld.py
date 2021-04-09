from flask import Flask, request, jsonify
import os
import json

hostname = os.uname()[1]
port = int(os.getenv('WEB_PORT', 8000))

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World from</h1> ' + hostname 

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True) 
