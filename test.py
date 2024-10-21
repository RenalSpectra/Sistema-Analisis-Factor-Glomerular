from config import supabase
from models import calculate_ifg


response = supabase.auth.sign_in_with_password({'email':'renalspectra@gmail.com', 'password':'rSP3CTR@'})
session = supabase.auth.get_session()

'''try:
    patient1 = {
        'ci': '5195292',
        'name': 'Alvaro',
        'lastname': 'Viamont Rico',
        'birthdate': '1991/12/03',
        'age': '33',
        'gender': 'M',
        'weight': '96.5',
        'height': '1.70'
    }
    supabase.table('patient').insert(patient1).execute()
    patient2 = {
        'ci': '5278670',
        'name': 'Jessica',
        'lastname': 'Orihuela Rojas',
        'birthdate': '1996/03/13',
        'age': '28',
        'gender': 'F',
        'weight': '85',
        'height': '1.60'
    }
    supabase.table('patient').insert(patient2).execute()
except Exception as e:
    print(e)

patients = supabase.table('patient').select('ci, name, lastname').execute()
if patients.data:
    for pat in patients.data:
        print(pat)
else:
    print('no existen pacientes')'''
ci = '5195292'
patient = supabase.table('patient').select('*').eq('ci', ci).execute()
age = patient.data[0]['age']
gender = patient.data[0]['gender']
height = patient.data[0]['height']
weight = patient.data[0]['weight']
ifg = calculate_ifg(566, age, gender, height, weight)

metric = {
        'creatine': 566,
        'ifg': ifg,
        'height': height,
        'weight': weight,
        'ci': ci
    }
metrics = supabase.table('metrics').insert(metric).execute()
if metrics.data:
    print(metrics)
else:
    print('No se insertó metrica')

response = supabase.auth.sign_out()

'''data = '12/03/1991'
print(data)
transform = data.split('/')
transform = '/'.join((transform[-1], transform[0], transform[1]))
print(transform)'''
