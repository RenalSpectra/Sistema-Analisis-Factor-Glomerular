from models import PDF
from app import app
from services import get_patient, get_metrics, get_all_patient
import os


img = os.path.join(app.root_path, 'static', 'icons', 'rinon.png')
save_path = os.path.join(app.root_path, 'static', 'pdfs')
all_patients = get_all_patient()
for patient in all_patients:
    ci = patient['ci']
    if ci == '7960527' or ci == '3603041':
        continue
    patient = get_patient(ci)[0]
    request_metrics = get_metrics(ci)
    metrics = request_metrics[0]['historical_metrics']
    metrics = metrics[::-1]
    metric = request_metrics[0]['latest_metric']
    pdf = PDF(patient, metric, metrics, img, save_path)
    pdf.build()


