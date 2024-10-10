from config import supabase
from models import calculate_ifg

# User management
def create_user(email, password):
    return supabase.auth.sign_up({'email': email, 'password': password})

# CRUD para PATIENT
def create_patient(data):
    return supabase.table('PATIENT').insert(data).execute()

def get_patient(ci):
    return supabase.table('PATIENT').select('*').eq('CI', ci).execute()

def update_patient(ci, data):
    return supabase.table('PATIENT').update(data).eq('CI', ci).execute()

def delete_patient(ci):
    return supabase.table('PATIENT').delete().eq('CI', ci).execute()

# CRUD para MEASURES
def create_measure(data):
    return supabase.table('MEASURES').insert(data).execute()

# CRUD para METRICS
def create_metric(data):
    patient = supabase.table('PATIENT').select('*').eq('CI', data['CI']).execute()
    if not patient.data:
        return {"error": "Patient not found"}, 404

    age = patient.data[0]['AGE']
    gender = patient.data[0]['GENDER']
    stature = data['STATURE']
    weight = data['WEIGHT']

    ifg = calculate_ifg(data['CREATINE'], age, gender, stature, weight)
    metric = {
        'CREATINE': data['CREATINE'],
        'IFG': ifg,
        'CI': data['CI'],
        'DATE': supabase.functions.now()
    }
    return supabase.table('METRICS').insert(metric).execute()

def get_metrics(ci, date=None):
    query = supabase.table('METRICS').select('*').eq('CI', ci)
    if date:
        query = query.eq('DATE', date)
    return query.execute()

def update_metric(ci, data):
    return supabase.table('METRICS').update(data).eq('CI', ci).execute()

def delete_metric(ci):
    return supabase.table('METRICS').delete().eq('CI', ci).execute()