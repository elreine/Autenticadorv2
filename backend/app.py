import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, abort
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO, send
import os
import secrets
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import re

# Cargar variables del archivo .env
load_dotenv()

# Variables de entorno
secret_key = os.getenv("SECRET_KEY", "clave_defecto")
firebase_key_path = os.getenv("FIREBASE_KEY_PATH", "backend/firebase_key.json")
env = os.getenv("ENV", "development")  # Define el entorno: 'development' o 'production'

# Configuración dinámica de Allowed Origins
if env == "production":
    allowed_origins = ["https://autenticadorv2-vert.vercel.app"]
else:
    allowed_origins = ["http://localhost", "http://127.0.0.1", "http://localhost:8080"]

# Configuración de Firebase
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configuración de Flask, Bcrypt y CORS
app = Flask(__name__)
CORS(app, origins=allowed_origins, supports_credentials=True)
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Configuración para WebSockets

# Almacén temporal para tokens generados y de sesión
generated_tokens = {}  # Tokens de registro
session_tokens = {}  # Tokens de sesión con expiración {"token": {"username": "user", "expires_at": datetime}}

# Middleware para verificar el origen en cada solicitud
@app.before_request
def check_origin():
    origin = request.headers.get("Origin")
    print(f"Cabeceras recibidas: {dict(request.headers)}")  # Registrar todas las cabeceras
    print(f"Origen detectado: {origin}")
    if origin and origin not in allowed_origins:
        abort(403, description="Acceso no autorizado")

# Ruta de inicio
@app.route('/')
def home():
    return jsonify({"message": "API de autenticación funcionando"}), 200

# Validar un token de sesión
@app.route('/validate-token', methods=['POST'])
def validate_token():
    session_token = request.headers.get("X-Session-Token")
    if not session_token or session_token not in session_tokens:
        return jsonify({"error": "Token no válido"}), 401

    # Verificar si el token ha expirado
    token_data = session_tokens.get(session_token)
    if token_data and token_data["expires_at"] < datetime.now(timezone.utc):
        del session_tokens[session_token]
        return jsonify({"error": "Token expirado"}), 401

    return jsonify({"message": "Token válido"}), 200

# Generar un token de registro seguro
@app.route('/generate-token', methods=['GET'])
def generate_token():
    try:
        token = secrets.token_hex(16)
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)
        generated_tokens[token] = expiration_time
        print(f"Token generado correctamente: {token}")
        return jsonify({"token": token}), 200
    except Exception as e:
        print(f"Error generando el token: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Registrar un usuario
@app.route('/register', methods=['POST'])
def register():
    registration_token = request.headers.get("X-Registration-Token")
    if not registration_token or registration_token not in generated_tokens:
        return jsonify({"error": "Token no válido o ausente"}), 403

    if generated_tokens[registration_token] < datetime.now(timezone.utc):
        del generated_tokens[registration_token]
        return jsonify({"error": "Token expirado"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    if not re.match("^[a-zA-Z0-9_]+$", username):
        return jsonify({"error": "Formato de usuario no permitido"}), 400

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_ref = db.collection('users').document(username)
        if user_ref.get().exists:
            return jsonify({"error": "El usuario ya existe"}), 409
        user_ref.set({"username": username, "password": hashed_password})
        del generated_tokens[registration_token]
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        print("Error en el registro:", e)
        return jsonify({"error": "Error en el servidor"}), 500

# Iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        user_ref = db.collection('users').document(username)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "Credenciales inválidas"}), 403

        user_data = user_doc.to_dict()

        if not bcrypt.check_password_hash(user_data['password'], password):
            return jsonify({"error": "Credenciales inválidas"}), 403

        session_token = secrets.token_hex(16)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)  # Token válido por 1 hora
        session_tokens[session_token] = {"username": username, "expires_at": expires_at}
        return jsonify({"token": session_token}), 200
    except Exception as e:
        print("Error al iniciar sesión:", e)
        return jsonify({"error": "Error en el servidor"}), 500

# Obtener usuarios registrados
@app.route('/users', methods=['GET'])
def get_users():
    session_token = request.headers.get("X-Session-Token")
    if not session_token or session_token not in session_tokens:
        return jsonify({"error": "Token de sesión inválido"}), 401

    token_data = session_tokens.get(session_token)
    if token_data and token_data["expires_at"] < datetime.now(timezone.utc):
        del session_tokens[session_token]
        return jsonify({"error": "Token expirado"}), 401

    try:
        users_ref = db.collection('users')
        users = [doc.to_dict() for doc in users_ref.stream()]
        return jsonify({"users": users}), 200
    except Exception as e:
        print("Error al recuperar usuarios:", e)
        return jsonify({"error": "Error en el servidor"}), 500

# Manejador global de errores
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Error: {e}")
    return jsonify({"error": "Error inesperado"}), 500

# Bloque principal
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
