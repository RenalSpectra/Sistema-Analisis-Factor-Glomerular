
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from config import supabase, SECRET_KEY
from services import create_user, get_patient, create_patient, update_patient, delete_patient, create_measure, get_metrics, create_metric, update_metric, delete_metric

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

# Control de acceso - login y creación de usuario (solo admins)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = supabase.auth.sign_in_with_password(email=data['email'], password=data['password'])
    if user:
        access_token = create_access_token(identity=user['user']['email'])
        return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/create_user', methods=['POST'])
@jwt_required()
def register_user():
    current_user = get_jwt_identity()
    # Verificar si el usuario actual es admin
    if current_user != 'admin@example.com':  # Reemplaza con lógica de admin real
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
    return jsonify(result)

@app.route('/patients/<ci>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_patient(ci):
    if request.method == 'GET':
        return jsonify(get_patient(ci))
    elif request.method == 'PUT':
        data = request.json
        return jsonify(update_patient(ci, data))
    elif request.method == 'DELETE':
        return jsonify(delete_patient(ci))

# CRUD para MEASURES
@app.route('/measures', methods=['POST'])
@jwt_required()
def add_measure():
    data = request.json
    return jsonify(create_measure(data))

# CRUD para METRICS - solo los usuarios pueden hacer RUD
@app.route('/metrics', methods=['POST'])
def add_metric():
    data = request.json
    # No requiere autenticación porque es enviado por el controlador ESP32
    return jsonify(create_metric(data))

@app.route('/metrics/<ci>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_metrics(ci):
    if request.method == 'GET':
        date = request.args.get('date')
        return jsonify(get_metrics(ci, date))
    elif request.method == 'PUT':
        data = request.json
        return jsonify(update_metric(ci, data))
    elif request.method == 'DELETE':
        return jsonify(delete_metric(ci))

if __name__ == '__main__':
    app.run(debug=True)
