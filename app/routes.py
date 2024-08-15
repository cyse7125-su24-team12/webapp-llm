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

@main.route('/generate', methods=['GET','HEAD','PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def healthz_method_not_allowed():
    return jsonify({"error": "Method not allowed"}), 405 

@main.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello, world!"})

@main.route('/', methods=['POST','HEAD','PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def healthz_method_not_allowed():
    return jsonify({"error": "Method not allowed"}), 405 

@main.route('/healthz', methods=['GET'])
def healthz():
    return '', 200

@main.route('/healthz', methods=['POST','HEAD','PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def healthz_method_not_allowed():
    return jsonify({"error": "Method not allowed"}), 405 

@main.app_errorhandler(404)
def page_not_found(error):
    return '', 404 