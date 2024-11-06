from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import supabase, SECRET_KEY, ADMIN
from services import create_user, get_patient, create_patient, update_patient, delete_patient, get_all_patient, get_metrics, create_metric, create_pdf

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
CORS(app, supports_credentials=True)

# Ruta para registrar usuarios (solo admins)
@app.route('/')
def init():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        data = request.json
        email = data['email']
        password = data['password']
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        try:
            # Iniciar sesión con el usuario en Supabase (o el sistema que uses)
            supabase.auth.sign_in_with_password({'email': email, 'password': password})
            user = supabase.auth.get_session()
            access_token = user.access_token
            # Crear la respuesta y agregar la cookie
            return jsonify({
            'message': 'Logged in successfully',
            'access_token': access_token,
            'redirect_url': '/home_admin'
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/home_admin', methods=['GET'])
def home_admin():
    if supabase.auth.get_session():
        return render_template('home-admin.html')
    else:
        return render_template('403.html')

# Ruta para cerrar sesión (logout)
@app.route('/logout', methods=['POST'])
def logout():
    try:
        # No se necesita una operación explícita en Supabase, simplemente invalidamos el token JWT en el frontend
        supabase.auth.sign_out()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta para crear usuarios (solo para admins)
@app.route('/create_user', methods=['POST'])
def register_user():
    log_user = supabase.auth.get_session()
    if log_user and log_user.user.email == ADMIN:
        data = request.json
        user = create_user(data['email'], data['password'])
        if user:
            return jsonify({"message": "User created successfully"}), 201
        return jsonify({"error": "User creation failed"}), 400
    else:
        return render_template('403.html')

# CRUD para PATIENT
@app.route('/patients', methods=['GET', 'POST'])
def add_patient():
    if supabase.auth.get_session():
        if request.method == 'GET':
            return render_template ('add-patient.html')
        if request.method == 'POST':
                data = request.json
                result = create_patient(data)
                return jsonify(result[0]), result[1]
    else:
        return render_template('403.html')

@app.route('/admin_search', methods=['GET', 'POST'])
def search_patient():
    if supabase.auth.get_session():
        if request.method == 'GET':
            return render_template('admin-search-patients.html')
        if request.method == 'POST':
            data = request.json
            print(f"Data received: {data}")  # Verifica los datos recibidos

            if 'patient' not in data:
                return jsonify({'error': 'No patient provided'}), 400

            if data['patient'] == 'all':
                all_patients = get_all_patient()  # Ahora devuelve directamente los datos
                print(f"All patients data: {all_patients}")  # Verifica los datos extraídos
                return jsonify(all_patients), 200  # Devuelve solo los datos

            else:
                patient = get_patient(data['patient'])  # Ahora devuelve directamente los datos
                print(f"Patient data: {patient}")  # Verifica los datos extraídos
                return jsonify(patient), 200  # Devuelve solo los datos

    else:
        return render_template('403.html'), 403

@app.route('/patients/<ci>', methods=['GET', 'PATCH', 'DELETE'])
def handle_patient(ci):
    if supabase.auth.get_session():
        if request.method == 'GET':
            return render_template('admin-info-patient.html')
        elif request.method == 'PATCH':
            data = request.json
            return jsonify(update_patient(ci, data)), 200
        elif request.method == 'DELETE':
            return jsonify(delete_patient(ci)), 200
    else:
        return render_template('403.html')
    
@app.route('/modifyPatient', methods=['GET', 'PUT'])
def modify_patient():
    if supabase.auth.get_session():
        if request.method == 'GET':
            return render_template('modify-patient.html')
        # elif request.method == 'PUT':
        #     data = request.json
        #     return jsonify(update_patient(ci, data)), 200
    else:
        return render_template('403.html')
    

# CRUD para METRICS - solo los usuarios pueden hacer RUD
@app.route('/api/metrics', methods=['POST'])
def add_metric():
    data = request.json
    if data['code'] == 'esp32espectra':
        response = create_metric(data)
        return jsonify(response[0]), response[1]
    else:
        return {"error": "Servicio no autorizado"}, 403

@app.route('/metrics/<ci>', methods=['GET', 'POST'])
def handle_metrics(ci):
    if supabase.auth.get_session():
        if request.method == 'GET':
            return render_template('analytics.html')
        if request.method == 'POST':
            data = request.json
            if data['type'] == 'actualizar':
                result = get_metrics(ci)
                return jsonify(result[0]), result[1]
            else:
                return jsonify(create_pdf(ci)), 200
    else:
        return render_template('403.html')

@app.route('/patient_search', methods=['GET', 'POST'])
def patient_search_patient():
    if request.method == 'GET':
        return render_template('patient-search-patients.html')
    if request.method == 'POST':
        return jsonify()

@app.route('/patient_metrics', methods=['GET', 'POST'])
def patient_handle_metrics():
    if request.method == 'GET':
        return render_template('patient-analytics.html')
        # return render_template('403.html')
    if request.method == 'POST':
        data = request.json
        result = get_metrics(data['ci'])
        return jsonify(result[0]), result[1]
        