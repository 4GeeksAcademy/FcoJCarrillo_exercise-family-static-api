"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")  # Create the jackson family object


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET', 'POST'])
def handle_hello():
    response_body = {}
    members = jackson_family.get_all_members()
    if request.method == 'GET':
        response_body = {"hello": "world",
                        "family": members}
    if request.method == 'POST':
        data = request.json
        members.append(data)
        response_body['result'] = members
    return jsonify(response_body), 200


@app.route('/members/<int:id>', methods=['GET', 'DELETE', 'POST'])
def handle_member(id):
    response_body = {}
    
    if request.method == 'GET':
        member = jackson_family.get_member(id)
        if not member:
            response_body['message'] = f'Fallo, usuario con id {id} no encontrado'
            return jsonify(response_body), 404

        response_body = {"message": f"Datos usuario",
                         "results": member}
        return jsonify(response_body), 200
    
    if request.method == 'DELETE':
        members1 = jackson_family.delete_member(id)
        print(members1)
        if not members1:
            response_body['message'] = f'Fallo al borrar el usuario con id {id} no encontrado'
            return jsonify(response_body),404
        
        response_body = {"done": True}
        return jsonify(response_body),200
    
# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
