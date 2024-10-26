def calculate_creatine (frecuency):
    pass

def calculate_ifg(creatine, age, gender, stature, weight):
    # Fórmula para calcular IFG
    # creatinina 415 - 680
    # Saludable 565 - 630
    if gender == 'M':
        return (140 - int(age)) * float(weight) / (72 * creatine)
    else:
        return (140 - int(age)) * float(weight) / (85 * creatine)
    
def calculate_ifg_ckd_epi(creatine, age, gender):
    tfg = None
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
    return tfg