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

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "first_name": "John",
    "last_name": "Jackson",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "last_name": "Jackson",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "last_name": "Jackson",
    "age": 5,
    "lucky_numbers": [1]
})

# Rutas de la API
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data or 'first_name' not in data or 'age' not in data or 'lucky_numbers' not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_member = {
        "id": jackson_family._generate_id(),
        "first_name": data['first_name'],
        "last_name": "Jackson",
        "age": data['age'],
        "lucky_numbers": data['lucky_numbers']
    }
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
