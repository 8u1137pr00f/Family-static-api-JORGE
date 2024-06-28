from flask import Flask, request, jsonify
from datastructures import FamilyStructure

app = Flask(__name__)

# Inicializamos la familia Jackson con miembros iniciales
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
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
        "first_name": data['first_name'],
        "age": data['age'],
        "lucky_numbers": data['lucky_numbers']
    }
    if 'id' in data:
        new_member['id'] = data['id']
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
