from flask import jsonify
from app.api import api_bp
from app.models.example import ExampleModel

@api_bp.route('/hello')
def hello():
    example = ExampleModel("a Flask Application")
    return jsonify({'message': f'Hello, I am {example.name}!'})
