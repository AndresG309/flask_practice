from flask import Flask, jsonify, request, render_template, redirect, url_for, abort, session

app = Flask(__name__)
# Crear secret key para trabajar con Sessions (Funciona en base a cookies encriptadas con la clave)
app.secret_key="1c47b6bc9f055fd6ba14f40246f145723a2ee70d71bde0357fa90951e3d72404"


# ------------------- RUTAS Y PLANTILLAS ----------
@app.route('/')
def inicio():
    # Esto se hace con la session
    if "username" not in session:
        return redirect(url_for("login"))
    
    return render_template('index.html', name=session["username"])
        

@app.route("/mostrar/<string:nombre>")
def page2(nombre):
    return render_template('mostrar.html', nombre=nombre)

# Múltiples rutas que usan una misma función
@app.route("/redireccion")
@app.route("/redireccion/extendida")
def redireccion():
    return redirect(url_for("page"))

@app.route("/error")
def error():
    # 401 -> Sin autorización
    return abort(401)
    # 404 -> Not Found
    return abort(404)


# ---------------- SESIONES -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    #  Hacemos diferenciación entre get y post ya que en el HTML no definimos el "action" del formulario, lo que termina llamando a la misma página donde está
    if request.method=="POST":
        session["username"] = request.form["username"]
        return redirect(url_for("inicio"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    redirect(url_for("inicio"))


# ----------------- CONTROL DE ERRORES --------
@app.errorhandler(404)
def error_not_found(error):
    # Devolver página y también código de error porque sino el cliente piensa que fue 200 (ya que la página se renderizó correctamente)
    return render_template("404.html", error=error), 404


# ------------------- MÉTODOS -------------------
@app.route("/metodos/get-post", methods=["GET", "POST"])
def get_post():
    return render_template("mensaje.html", mensaje="Página de get y post")
@app.route("/metodos/delete", methods=["DELETE"])
def delete():
    return render_template("mensaje.html", mensaje="Página de delete")
@app.route("/metodos/put-patch", methods=["PUT", "PATCH"])
def put_patch():
    return render_template("mensaje.html", mensaje="Página de put y patch")


# ----------------- CRUD -------------------
# Database
users = []
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