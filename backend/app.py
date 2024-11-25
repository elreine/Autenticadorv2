import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import re
import os
from itsdangerous import URLSafeTimedSerializer
import secrets
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Variables de entorno
secret_key = os.getenv("SECRET_KEY", "clave_defecto")
firebase_key_path = os.getenv("FIREBASE_KEY_PATH", "backend/firebase_key.json")
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1").split(",")

# Configuración de Firebase
if "RENDER" in os.environ:
    # Si está en Render, usa la ruta del archivo secreto
    cred = credentials.Certificate("/etc/secrets/firebase_key.json")
else:
    # Si está ejecutándose localmente, usa la ruta configurada en .env
    cred = credentials.Certificate(firebase_key_path)

firebase_admin.initialize_app(cred)
db = firestore.client()

# Configuración de Flask, Bcrypt y CORS
app = Flask(__name__)
CORS(app, origins=allowed_origins)
bcrypt = Bcrypt(app)

# Configuración del generador de tokens CSRF
csrf_serializer = URLSafeTimedSerializer(secret_key)

# Ruta de inicio para evitar 404 en la raíz
@app.route('/')
def home():
    return "API de autenticación funcionando"

# Ruta para generar el token CSRF
@app.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    token = csrf_serializer.dumps("csrf_token")
    return jsonify({"csrf_token": token})

# Ruta para el registro de usuario con verificación de token CSRF
@app.route('/register', methods=['POST'])
def register():
    # Obtener el token enviado desde el cliente
    token = request.headers.get("X-Auth-Token")

    # Validar el token
    if not token or len(token) != 32:  # Verificamos que el token sea válido
        return jsonify({"error": "Token no válido o ausente"}), 403

    # Validar que la solicitud provenga de un origen permitido
    origin = request.headers.get("Origin")
    if origin not in allowed_origins:
        return jsonify({"error": "Acceso no autorizado"}), 403

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

# Ruta para generar un token seguro
@app.route('/generate-token', methods=['GET'])
def generate_token():
    # Generar un token único y seguro
    token = secrets.token_hex(16)  # Genera un token hexadecimal de 32 caracteres
    return jsonify({"token": token})

# Manejador global de errores
@app.errorhandler(Exception)
def handle_exception(e):
    # Registrar el error internamente
    print(f"Error: {e}")
    # Respuesta genérica para el cliente
    return jsonify({"error": "Ocurrió un problema. Por favor, intenta de nuevo."}), 500

# Bloque principal
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
