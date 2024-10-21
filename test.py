from config import supabase


response = supabase.auth.sign_in_with_password({'email':'renalspectra@gmail.com', 'password':'rSP3CTR@'})
session = supabase.auth.get_session()

try:
    patient = {
        'ci': '5195292',
        'name': 'Alvaro',
        'lastname': 'Viamont Rico',
        'birthdate': '1991/12/03',
        'age': '33',
        'gender': 'M',
        'weight': '96.5',
        'height': '1.70'
    }
    supabase.table('patient').insert(patient).execute()
except Exception as e:
    print(e)


response = supabase.auth.sign_out()

'''data = '12/03/1991'
print(data)
transform = data.split('/')
transform = '/'.join((transform[-1], transform[0], transform[1]))
print(transform)'''
