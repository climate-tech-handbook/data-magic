from flask import jsonify
from app.api import api_bp

@api_bp.route('/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})
