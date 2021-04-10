from flask import Flask, request, jsonify
from routes import configure_routes
import os

port = int(os.getenv('WEB_PORT', 8000))

app = Flask(__name__)


configure_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True) 
