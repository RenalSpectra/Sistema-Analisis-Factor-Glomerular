import os
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
import numpy as np
import tempfile

def calculate_ifg(creatine, age, gender, stature, weight):
    if gender == 'M':
        return (140 - int(age)) * float(weight) / (72 * creatine)
    else:
        return (140 - int(age)) * float(weight) / (85 * creatine)
    
def calculate_ifg_ckd_epi(creatine, age, gender):
    tfg = None
    creatine = float(creatine)
    age = float(age)
    if gender == 'F':
        if creatine <= 0.7:
            tfg = 144 * ((creatine/0.7)**-0.329) * (0.993**age)
        else:
            tfg = 144 * ((creatine/0.7)**-1.209) * (0.993**age)
    else:
        if creatine <= 0.9:
            tfg = 141 * ((creatine/0.9)**-0.411) * (0.993**age)
        else:
            tfg = 141 * ((creatine/0.9)**-1.209) * (0.993**age)
    return round(tfg, 2)

class PDF(FPDF):
    def __init__(self, patient, metric, metrics, img, save_path):
        super().__init__()
        self.current_date = datetime.today().strftime("%d/%m/%Y")
        self.patient = patient
        self.metric = metric
        self.dates = [] #datetime.strptime(m['date'], '%Y-%m-%d').strftime('%d/%m/%Y') for m in metrics
        for m in metrics:
            date_str = m['date']
            try:
                date_obj = datetime.strptime(date_str, '%Y/%m/%d')
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    continue
            self.dates.append(date_obj.strftime('%d/%m/%Y'))
        self.ifg_values = [float(m['ifg']) for m in metrics]
        self.weight_values = [float(m['weight']) for m in metrics]
        self.logo_path = img
        self.save_path = save_path
    
    def header (self):
        self.set_fill_color(24, 36, 74)
        self.rect(0, 0, self.w, 20, 'F') 

        self.set_xy(170, 5)
        self.set_text_color(255, 255, 255)
        self.set_font('Times', '', 12)
        self.cell(0, 10, f"Fecha: {self.current_date}", 0, 1, 'R')

        self.image(self.logo_path, 10, 5, 12)
        self.set_xy(50, 8)
        self.set_text_color(14, 161, 213)
        self.set_font('Times', 'B', 45)
        y = self.get_y()
        self.set_xy(25, y-2)
        self.cell(0, 10, 'RenalSpectra', ln=True)
        self.ln(8)

    def footer (self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.set_text_color(82, 81, 81)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
    
    def _patient_section (self):
        self.set_font("Times", "B", 24)
        self.set_text_color(14, 161, 213)
        self.cell(0, 10, "Reporte", 0, 1, "C")

        self.set_font("Times", "B", 16)
        self.set_text_color(14, 161, 213)
        self.cell(0, 10, "Datos del paciente:", 0, 1)
        
        self.set_font("Times", "", 12)
        self.set_text_color(43, 43, 43)
        self.cell(0, 10, f"CI: {self.patient['ci']}")
        self.ln(8)
        self.cell(0, 10, f"Nombre: {self.patient['name']} {self.patient['lastname']}")
        self.ln(8)
        y = self.get_y()
        x = self.get_x()
        self.cell(0, 10, f"Edad: {self.patient['age']}")
        self.set_xy(x+70, y)
        self.cell(0, 10, f"Género: {self.patient['gender']}")
        self.set_xy(x, y)
        self.ln(8)
        y = self.get_y()
        x = self.get_x()
        self.cell(0, 10, f"Peso actual: {self.patient['weight']}")
        self.set_xy(x+70, y)
        self.cell(0, 10, f"Altura actual: {self.patient['height']}")
        self.set_xy(x, y)
        self.ln(10)
        self.set_draw_color(82, 81, 81) 
        self.cell(0, 10, "_" * 100, 0, 1, "C")
    
    def estadio (self, ifg):
        ifg = float(ifg)
        if ifg >= 90:
            return '1', 'Posible daño renal con función renal normal', (76, 175, 80)
        if ifg < 90 and ifg >= 60:
            return '2', 'Daño renal con disminución leve de la función renal', (255, 235, 59)
        if ifg < 60 and ifg >= 45:
            return '3a', 'Disminución de leve a moderada de la función renal', (255, 152, 0)
        if ifg < 45 and ifg >= 30:
            return '3b', 'Disminución de moderada a grave de la función renal', (255, 152, 0)
        if ifg < 30 and ifg >= 15:
            return '4', 'Disminución grave de la función renal', (255, 152, 0)
        if ifg < 15:
            return '5', 'Insuficiencia renal', (244, 67, 54)
    
    def _analytic_section (self):
        self.set_font("Times", "B", 16)
        self.set_text_color(14, 161, 213)
        self.cell(0, 10, "Analíticas", 0, 1)
        
        self.set_font("Times", "", 12)
        self.set_text_color(43, 43, 43) 
        try:
            # Intenta con el formato de guiones
            date_obj = datetime.strptime(self.metric['date'], '%Y-%m-%d')
        except ValueError:
            try:
                # Si falla, intenta con el formato de barras inclinadas
                date_obj = datetime.strptime(self.metric['date'], '%Y/%m/%d')
            except ValueError:
                # Si no coincide con ningún formato, usa una fecha predeterminada
                date_obj = datetime.now()
        formatted_date = date_obj.strftime('%d/%m/%Y')
        
        # self.cell(0, 10, f"Fecha ultimo análisis: {datetime.strptime(self.metric['date'], '%Y-%m-%d').strftime('%d/%m/%Y')}")
        self.cell(0, 10, f"Fecha ultimo análisis: {formatted_date}")
        self.ln(8)
        color = self.estadio(self.metric['ifg'])[2]
        self.set_fill_color(color[0], color[1], color[2]) 
        y = self.get_y()
        self.rect(0, y, 40, 9, 'F')
        self.cell(0, 10, f"Estadio: {self.estadio(self.metric['ifg'])[0]}")
        self.ln(8)
        y = self.get_y()
        x = self.get_x()
        self.cell(0, 10, f"Creatinina: {self.metric['creatine']} mg/dl")
        self.set_xy(x+70, y)
        self.cell(0, 10, f"IFG: {self.metric['ifg']} mL/min/1.73 m²")
        self.set_xy(x, y)
        self.ln(8)
        self.cell(0, 10, f"Descripción: {self.estadio(self.metric['ifg'])[1]}")
        self.ln(10)
    
    def _grafic_section(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.tight_layout(pad=6)
        min_y= min(min(self.ifg_values), min(self.weight_values)) - 1 
        max_y = max(max(self.ifg_values), max(self.weight_values)) + 1
        ax.set_ylim(min_y, max_y)
        ax.plot(self.dates, self.ifg_values, color='#0E72C9', label='IFG', marker='o', linestyle='-')
        ax.bar(self.dates, self.weight_values, color='#066405', alpha=0.5, label='Peso', width=0.8)
        plt.title("Evolución de IFG", color='#273C7B', fontsize=24)
        ax.set_xlabel('Fecha (dia/mes/año)', fontsize=12)
        ax.set_ylabel('IFG: mL/min/1.73 m² / Peso: Kg', fontsize=12)
        ax.grid(True)
        ax.set_xticks(self.dates)
        ax.set_xticklabels([date for date in self.dates], rotation=60, ha='right')
        ax.legend(loc='upper right', fontsize=10, frameon=True)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            fig.savefig(temp_file.name, format='png')
            plt.close(fig)
            self.image(temp_file.name, x=10, y=None, w=180)
    
    def build (self):
        self.add_page()
        self._patient_section()
        self._analytic_section()
        self._grafic_section()
        output_path = os.path.join(self.save_path, f"Reporte_Paciente_{self.patient['ci']}.pdf")
        self.output(output_path)
        return output_path