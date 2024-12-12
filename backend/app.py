import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, abort
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import secrets
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import re

# Cargar variables desde el archivo .env del backend si no están ya definidas
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Variables de entorno
secret_key = os.getenv("SECRET_KEY", "clave_defecto")
firebase_key_path = os.getenv("FIREBASE_KEY_PATH", "backend/firebase_key.json")
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
env = os.getenv("ENV", "development")

# Configuración de Firebase
try:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase conectado correctamente")
except Exception as e:
    print(f"Error al conectar con Firebase: {e}")
    db = None

# Configuración de Flask, Bcrypt y CORS
app = Flask(__name__)
CORS(app, origins=allowed_origins, supports_credentials=True)
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Almacén temporal para tokens generados y de sesión
generated_tokens = {}
session_tokens = {}

# Middleware para verificar el origen
@app.before_request
def check_origin():
    origin = request.headers.get("Origin")
    if env == "development":
        print(f"Cabeceras recibidas: {dict(request.headers)}")
        print(f"Origen detectado: {origin}")
    if origin and origin not in allowed_origins:
        abort(403, description="Acceso no autorizado")

@app.route('/')
def home():
    return jsonify({"message": "API de autenticación funcionando"}), 200

@app.route('/validate-token', methods=['POST'])
def validate_token():
    session_token = request.headers.get("X-Session-Token")
    print(f"Token recibido en /validate-token: {session_token}")
    if not session_token or session_token not in session_tokens:
        return jsonify({"error": "Token no válido"}), 401

    token_data = session_tokens.get(session_token)
    if token_data and token_data["expires_at"] < datetime.now(timezone.utc):
        del session_tokens[session_token]
        return jsonify({"error": "Token expirado"}), 401

    return jsonify({"message": "Token válido"}), 200

@app.route('/generate-token', methods=['GET'])
def generate_token():
    try:
        token = secrets.token_hex(16)
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)
        generated_tokens[token] = expiration_time
        print(f"Token generado correctamente: {token}")
        return jsonify({"token": token}), 200
    except Exception as e:
        print(f"Error en /generate-token: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        registration_token = request.headers.get("X-Registration-Token")
        print(f"Token de registro recibido: {registration_token}")
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

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_ref = db.collection('users').document(username)
        if user_ref.get().exists:
            return jsonify({"error": "El usuario ya existe"}), 409
        user_ref.set({"username": username, "password": hashed_password})
        del generated_tokens[registration_token]
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        print(f"Error en /register: {e}")
        return jsonify({"error": "Error en el servidor"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        print("Iniciando proceso de inicio de sesión...")

        # Datos recibidos del cliente
        data = request.get_json()
        print(f"Datos recibidos: {data}")

        # Validar datos de entrada
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            print("Error: Datos incompletos")
            return jsonify({"error": "Datos incompletos"}), 400

        # Buscar usuario en Firebase
        print(f"Buscando usuario: {username}")
        user_ref = db.collection('users').document(username)
        user_doc = user_ref.get()

        if not user_doc.exists:  # Ajustado: Cambiado de exists() a exists
            print("Error: Usuario no encontrado")
            return jsonify({"error": "Credenciales inválidas"}), 403

        user_data = user_doc.to_dict()
        print(f"Datos del usuario recuperados: {user_data}")

        # Validar existencia de contraseña
        if 'password' not in user_data:
            print("Error: Contraseña no encontrada en los datos del usuario")
            return jsonify({"error": "Error interno del servidor"}), 500

        # Validar contraseña
        if not bcrypt.check_password_hash(user_data['password'], password):
            print("Error: Contraseña inválida")
            return jsonify({"error": "Credenciales inválidas"}), 403

        # Generar token de sesión
        session_token = secrets.token_hex(16)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session_tokens[session_token] = {"username": username, "expires_at": expires_at}
        print(f"Token de sesión generado: {session_token} para usuario: {username}")

        return jsonify({"token": session_token}), 200
    except Exception as e:
        print(f"Error en /login: {e}")
        return jsonify({"error": "Error inesperado al procesar la solicitud."}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        session_token = request.headers.get("X-Session-Token")
        print(f"Token de sesión recibido en /users: {session_token}")
        if not session_token or session_token not in session_tokens:
            return jsonify({"error": "Token de sesión inválido"}), 401

        token_data = session_tokens.get(session_token)
        if token_data and token_data["expires_at"] < datetime.now(timezone.utc):
            del session_tokens[session_token]
            return jsonify({"error": "Token expirado"}), 401

        users_ref = db.collection('users')
        users = [doc.to_dict() for doc in users_ref.stream()]
        return jsonify({"users": users}), 200
    except Exception as e:
        print(f"Error en /users: {e}")
        return jsonify({"error": "Error en el servidor"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Manejo global de errores"""
    print(f"Error inesperado: {e}")  # Registrar detalles en consola
    return jsonify({"error": "Ocurrió un error interno. Consulte al administrador del sistema."}), 500

if __name__ == '__main__':
    print(f"Entorno actual: {env}")
    print(f"Allowed Origins: {allowed_origins}")

    # Configurar host y modo de depuración según el entorno
    host = '127.0.0.1' if env == 'development' else '0.0.0.0'
    debug = (env == 'development')

    # Ejecutar la aplicación
    app.run(host=host, port=5000, debug=debug)