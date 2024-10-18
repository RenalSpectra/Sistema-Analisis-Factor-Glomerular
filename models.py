def calculate_ifg(creatine, age, gender, stature, weight):
    # Fórmula para calcular IFG
    # creatinina 415 - 680
    # Saludable 565 - 630
    if gender == 'M':
        return (140 - age) * weight / (72 * creatine)
    else:
        return (140 - age) * weight / (85 * creatine)