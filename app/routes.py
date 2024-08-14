from flask import Blueprint, request, jsonify
from .model import generate_response

main = Blueprint('main', __name__)

@main.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response = generate_response(prompt)
    return jsonify({"response": response})

@main.route('/')
def index():
    return jsonify({"message": "Hello, world!"})
