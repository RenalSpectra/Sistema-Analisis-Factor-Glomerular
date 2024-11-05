from config import supabase
from models import calculate_ifg

# User management
def create_user(email, password):
    return supabase.auth.sign_up({'email': email, 'password': password})

# CRUD para PATIENT
def create_patient(data):
    try:
        existing_patient = supabase.table('patient').select('*').eq('ci', data['ci']).execute()
        if existing_patient.data:
            return {'error': 'Patient with this CI already exists'}, 400
        response = supabase.table('patient').insert(data).execute()
        if not response.data:
            return {'error': 'Failed to add patient'}, 400
        return {'patient': response.data}, 201
    except Exception as e:
        return {'error': str(e)}, 400

def get_all_patient():
    response = supabase.table('patient').select('ci, name, lastname').execute()
    return response.data  # Devolver solo los datos

def get_patient(ci):
    response = supabase.table('patient').select('*').eq('ci', ci).execute()
    return response.data  # Devolver solo los datos

def update_patient(ci, data):
    response =  supabase.table('patient').update(data).eq('ci', ci).execute()
    return response.data

def delete_patient(ci):
    response =  supabase.table('patient').delete().eq('ci', ci).execute()
    return response.data

# CRUD para METRICS
def create_metric(data):
    patient = supabase.table('patient').select('*').eq('ci', data['ci']).execute()
    if not patient.data:
        return {"error": "Patient not found"}, 404
    age = patient.data[0]['age']
    gender = patient.data[0]['gender']
    height = patient.data[0]['height']
    weight = patient.data[0]['weight']
    ifg = calculate_ifg(data['creatine'], age, gender, height, weight)
    metric = {
        'creatine': data['creatine'],
        'ifg': ifg,
        'height': height,
        'weight': weight,
        'ci': data['ci']
    }
    response = supabase.table('metrics').insert(metric).execute()
    return response.data, 201

def get_metrics(ci, date=None):
    query = supabase.table('metrics').select('*').eq('ci', ci)
    if date:
        query = query.eq('date', date)
    response =  query.execute()
    return response.data

def update_metric(ci, data):
    response = supabase.table('metrics').update(data).eq('ci', ci).execute()
    return response.data

def delete_metric(ci):
    resposne = supabase.table('metrics').delete().eq('ci', ci).execute()
    return resposne.data

def create_pdf(ci):
    pass