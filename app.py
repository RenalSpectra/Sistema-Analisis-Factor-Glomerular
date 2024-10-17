from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from config import supabase, SECRET_KEY, ADMIN
from services import create_user, get_patient, create_patient, update_patient, delete_patient, create_measure, get_metrics, create_metric, update_metric, delete_metric

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

# Ruta para registrar usuarios (solo admins)
@app.route('/')
def init():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
@jwt_required()
def signup():
    current_user = get_jwt_identity()
    if current_user != ADMIN:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    email = data['email']
    password = data['password']

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        # Crear el usuario en Supabase
        response = supabase.auth.sign_up({'email': email, 'password': password})
        return jsonify({'message': 'User registered successfully', 'user': response}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta para iniciar sesión (login)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        # Iniciar sesión con el usuario en Supabase
        response = supabase.auth.sign_in_with_password({'email': email, 'password': password})
        user = response['user']
        access_token = create_access_token(identity=user['id'])

        return jsonify({'message': 'Logged in successfully', 'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta para cerrar sesión (logout)
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # No se necesita una operación explícita en Supabase, simplemente invalidamos el token JWT en el frontend
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta para crear usuarios (solo para admins)
@app.route('/create_user', methods=['POST'])
@jwt_required()
def register_user():
    current_user = get_jwt_identity()
    # Verificar si el usuario actual es admin
    if current_user != ADMIN: 
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.json
    user = create_user(data['email'], data['password'])
    if user:
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"error": "User creation failed"}), 400

# CRUD para PATIENT
@app.route('/patients', methods=['POST'])
@jwt_required()
def add_patient():
    data = request.json
    result = create_patient(data)
    return jsonify(result), 201

@app.route('/patients/<ci>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_patient(ci):
    if request.method == 'GET':
        return jsonify(get_patient(ci)), 200
    elif request.method == 'PUT':
        data = request.json
        return jsonify(update_patient(ci, data)), 200
    elif request.method == 'DELETE':
        return jsonify(delete_patient(ci)), 200

# CRUD para MEASURES
@app.route('/measures', methods=['POST'])
@jwt_required()
def add_measure():
    data = request.json
    return jsonify(create_measure(data)), 201

# CRUD para METRICS - solo los usuarios pueden hacer RUD
@app.route('/metrics', methods=['POST'])
def add_metric():
    data = request.json
    # No requiere autenticación porque es enviado por el controlador ESP32
    return jsonify(create_metric(data)), 201

@app.route('/metrics/<ci>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_metrics(ci):
    if request.method == 'GET':
        date = request.args.get('date')
        return jsonify(get_metrics(ci, date)), 200
    elif request.method == 'PUT':
        data = request.json
        return jsonify(update_metric(ci, data)), 200
    elif request.method == 'DELETE':
        return jsonify(delete_metric(ci)), 200

if __name__ == '__main__':
    app.run(debug=True)