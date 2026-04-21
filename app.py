from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Database
users = []

@app.route('/')
def page():
    return render_template('index.html', name="Andres")

# GET
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# POST
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")

    if name is None:
        return jsonify({"error": "Name is required"}), 400
    if name == "":
        return jsonify({"error": "Name cannot be empty"}), 400

    new_user = {"id": len(users)+1, "name": name}
    users.append(new_user)

    return jsonify(new_user), 201

# PUT
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    for usr in users:
        if usr["id"] == user_id:
            user = usr
            break
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    user["name"] = name

    return jsonify(user), 200

# DELETE
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    index = None
    for usr in users:
        if usr["id"] == user_id:
            index = users.index(usr)
            break
    if index is None:
        return jsonify({"error": "User not found"}), 404

    users.pop(index)

    return '', 204

if __name__=='__main__':
    app.run()