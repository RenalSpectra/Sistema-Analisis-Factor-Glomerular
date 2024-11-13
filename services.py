from config import supabase, ADMIN, PASSWORD
from models import calculate_ifg, calculate_ifg_ckd_epi, PDF

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
    # ifg = calculate_ifg(data['creatine'], age, gender, height, weight)
    ifg = calculate_ifg_ckd_epi(data['creatine'], age, gender)
    metric = {
        'creatine': data['creatine'],
        'ifg': ifg,
        'height': height,
        'weight': weight,
        'ci': data['ci']
    }
    if 'date' in data:
        metric['date'] = data['date']
    response = supabase.table('metrics').insert(metric).execute()
    return response.data, 201

def get_metrics(ci, date=None):
    patient = supabase.table('patient').select('*').eq('ci', ci).execute()
    if not patient.data:
        return {"error": "Paciente no encontrado."}, 404
    query = supabase.table('metrics').select('creatine, ifg, date, weight').eq('ci', ci)
    if date:
        query = query.eq('date', date)
    response = query.order('date', desc=True).execute()
    metrics = response.data
    if not metrics:
        return {"error": "No metrics found for this patient"}, 404

    patient_info = patient.data[0]
    latest_metric = metrics[0]
    historical_metrics = metrics
    result = {
        "patient_info": patient_info,
        "latest_metric": latest_metric,
        "historical_metrics": historical_metrics
    }
    return result, 201

def update_metric(ci, data):
    response = supabase.table('metrics').update(data).eq('ci', ci).execute()
    return response.data

def delete_metric(ci):
    resposne = supabase.table('metrics').delete().eq('ci', ci).execute()
    return resposne.data

def create_pdf(ci, img, save_path):
    patient = get_patient(ci)[0]
    request_metrics = get_metrics(ci)
    metrics = request_metrics[0]['historical_metrics'][::-1]
    metric = request_metrics[0]['latest_metric']
    pdf = PDF(patient, metric, metrics, img, save_path)
    return pdf.build()