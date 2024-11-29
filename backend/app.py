import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, abort
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import re
import os
from itsdangerous import URLSafeTimedSerializer
import secrets
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Cargar variables del archivo .env
load_dotenv()

# Variables de entorno
secret_key = os.getenv("SECRET_KEY", "clave_defecto")
firebase_key_path = os.getenv("FIREBASE_KEY_PATH", "backend/firebase_key.json")
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1,http://localhost:8080").split(",")

auth_key = os.getenv("AUTH_KEY", "clave_defecto")
print(f"AUTH_KEY cargada desde .env: {auth_key}")

# Configuración de Firebase
if "RENDER" in os.environ:
    cred = credentials.Certificate("/etc/secrets/firebase_key.json")
else:
    cred = credentials.Certificate(firebase_key_path)

firebase_admin.initialize_app(cred)
db = firestore.client()

# Configuración de Flask, Bcrypt y CORS
app = Flask(__name__)
CORS(app, origins=allowed_origins)
bcrypt = Bcrypt(app)

# Almacén temporal para tokens generados
generated_tokens = {}  # Estructura: {"token": expiration_time}
session_tokens = {}  # Estructura: {"session_token": username}

# Middleware para verificar el origen en cada solicitud
@app.before_request
def check_origin():
    origin = request.headers.get("Origin")
    if origin and origin not in allowed_origins:
        abort(403, description="Acceso no autorizado")

# Ruta de inicio
@app.route('/')
def home():
    return "API de autenticación funcionando"

# Ruta para generar un token seguro
@app.route('/generate-token', methods=['GET'])
def generate_token():
    auth_header_key = request.headers.get("X-Auth-Key")
    if auth_header_key != auth_key:
        return jsonify({"error": "Clave no válida"}), 403

    # Generar token único y asignar expiración
    token = secrets.token_hex(16)
    expiration_time = datetime.utcnow() + timedelta(minutes=10)  # Expira en 10 minutos
    generated_tokens[token] = expiration_time

    return jsonify({"token": token})

# Ruta para el registro de usuario
@app.route('/register', methods=['POST'])
def register():
    registration_token = request.headers.get("X-Registration-Token")
    if not registration_token or registration_token not in generated_tokens:
        return jsonify({"error": "Token no válido o ausente"}), 403

    # Verificar si el token ha expirado
    if generated_tokens[registration_token] < datetime.utcnow():
        del generated_tokens[registration_token]  # Eliminar el token expirado
        return jsonify({"error": "Token expirado"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan el nombre de usuario o la contraseña"}), 400

    if not re.match("^[a-zA-Z0-9_]+$", username):
        return jsonify({"error": "El nombre de usuario solo puede contener letras, números y guiones bajos"}), 400

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_ref = db.collection('users').document(username)
        user_ref.set({
            'username': username,
            'password': hashed_password
        })
        del generated_tokens[registration_token]  # Eliminar el token utilizado
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        print("Error en el registro:", e)
        return jsonify({"error": "Hubo un problema en el servidor"}), 500

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan el nombre de usuario o la contraseña"}), 400

    try:
        user_ref = db.collection('users').document(username)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "Credenciales incorrectas"}), 403

        user_data = user_doc.to_dict()

        if not bcrypt.check_password_hash(user_data['password'], password):
            return jsonify({"error": "Credenciales incorrectas"}), 403

        # Generar token de sesión
        session_token = secrets.token_hex(16)
        session_tokens[session_token] = username  # Guardar el token de sesión asociado al usuario
        return jsonify({"token": session_token}), 200
    except Exception as e:
        print("Error al iniciar sesión:", e)
        return jsonify({"error": "Hubo un problema en el servidor"}), 500

# Ruta para obtener usuarios registrados
@app.route('/users', methods=['GET'])
def get_users():
    session_token = request.headers.get("X-Session-Token")
    if not session_token or session_token not in session_tokens:
        return jsonify({"error": "Token de sesión requerido o no válido"}), 401

    try:
        users_ref = db.collection('users')
        users = [doc.to_dict() for doc in users_ref.stream()]
        return jsonify({"users": users}), 200
    except Exception as e:
        print("Error al recuperar usuarios:", e)
        return jsonify({"error": "Hubo un problema al obtener la lista de usuarios"}), 500

# Manejador global de errores
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Error: {e}")
    return jsonify({"error": "Ocurrió un problema. Por favor, intenta de nuevo."}), 500

# Bloque principal
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
