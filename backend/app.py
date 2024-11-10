import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import re
import os  # Importar para acceder a variables de entorno
from itsdangerous import URLSafeTimedSerializer

# Configuración de Flask, Bcrypt y CORS
app = Flask(__name__)
CORS(app, origins=["https://autenticadorv2.onrender.com"])
bcrypt = Bcrypt(app)

# Configuración del generador de tokens CSRF
secret_key = "mi_secreto_unico"
csrf_serializer = URLSafeTimedSerializer(secret_key)

# Configuración de Firebase
if "RENDER" in os.environ:
    # Si está en Render, usa la ruta del archivo secreto
    cred = credentials.Certificate("/etc/secrets/firebase_key.json")
else:
    # Si está ejecutándose localmente, usa la ruta local
    cred = credentials.Certificate("backend/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Ruta para generar el token CSRF
@app.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    token = csrf_serializer.dumps("csrf_token")
    return jsonify({"csrf_token": token})

# Ruta para el registro de usuario con verificación de token CSRF
@app.route('/register', methods=['POST'])
def register():
    # Obtener el token CSRF desde los encabezados de la solicitud
    token = request.headers.get("X-CSRF-Token")

    # Verificar el token
    try:
        csrf_serializer.loads(token, max_age=3600)  # Token válido por 1 hora
    except:
        return jsonify({"error": "Token CSRF no válido o expirado"}), 403

    # Obtener datos del usuario
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validación básica
    if not username or not password:
        return jsonify({"error": "Faltan el nombre de usuario o la contraseña"}), 400

    # Verificar que el nombre de usuario solo contenga letras y números
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return jsonify({"error": "El nombre de usuario solo puede contener letras, números y guiones bajos"}), 400

    try:
        # Encriptar la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Guardar en Firestore
        user_ref = db.collection('users').document(username)
        user_ref.set({
            'username': username,
            'password': hashed_password
        })

        return jsonify({"message": "Usuario registrado exitosamente", "username": username}), 201
    except Exception as e:
        print("Error en el registro:", e)
        return jsonify({"error": "Hubo un problema en el servidor"}), 500

# Ruta para obtener la lista de usuarios registrados
@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Recuperar todos los usuarios de la colección 'users' en Firestore
        users_ref = db.collection('users')
        users = [doc.to_dict() for doc in users_ref.stream()]
        return jsonify({"users": users}), 200
    except Exception as e:
        print("Error al recuperar usuarios:", e)
        return jsonify({"error": "Hubo un problema al obtener la lista de usuarios"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
