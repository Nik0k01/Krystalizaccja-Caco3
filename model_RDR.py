import math

def model_RDR(t, y, dane_init, dane_fiz):
    """
    Ta funkcja ma za zadanie zdefiniować układ równań różniczkowych zwyczajnych, opisujących
    krystalizację węglanu wapnia w reaktorze z obrotowymi dyskami
    """
    c_CO2 = y[0]
    c_CaOH = y[1]
    c_CaCO3 = y[2]
    crystal_d = y[3]
    crystal_No = y[4]
    
    # Rozmiar zarodka
    crystal_init_d = dane_init['d_init']
    # Gęstość kryształów - kg/m3
    crystal_density = dane_fiz['crystal_density']
    # Masa molowa kg/kmol
    molar_mass = dane_fiz['molar_mass']
    # Molar density mol/m3
    molar_density = crystal_density / molar_mass * 1000
    # Stała szybkości reakcji
    k = dane_fiz['k_rxn']
    # Wykładniki i stałe wzrostu i nukleacji
    n = dane_fiz['n']
    g = dane_fiz['g']
    k_g = dane_fiz['k_g']
    k_n = dane_fiz['k_nuc']
    
    # Maksymalne stężenie węglanu wapnia
    c_satur = math.sqrt(dane_fiz['k_sp'])
    
    # Szybkość wzrostu kryształu  zachodzi gdy stężenie przekroczy maksymalne
    if (c_CaCO3 - c_satur) > 0:
        cryst_growth = k_g * (c_CaCO3 - c_satur) ** g
    else:
        cryst_growth = 0
        
    # Szybkość nukleacji - zachodzi gdy stężenie przekroczy maksymalne
    if (c_CaCO3 - c_satur) > 0:
        cryst_nuc = k_n * (c_CaCO3 - c_satur) ** n   
    else:
        cryst_nuc = 0

    # Stężenie CO2 utzrymywane na stałym poziomie
    dCO2dt = 0
    # Zmiana stężenia zasady wapniowej - w wyniku reakcji 
    dCaOHdt = - k * c_CO2 * c_CaOH    
    # Mole węglanu pochłonięte na zarodkowanie
    nuc_mol = molar_density * math.pow(crystal_init_d, 3) * math.pi / 6 * cryst_nuc 
        
    # Uproszczone wyrażenie na ilość moli pochłoniętych na wzrost (pomijalna)
    crystal_dist = [(1, 30e-9)]
    growth_mol = 0
    for x in crystal_dist:
        growth_mol += math.pi * molar_density * x[0] * x[1] ** 2 * cryst_growth * crystal_No
    
    # Zmiana stężenia węglanu wapnia
    dCaCO3dt = -dCaOHdt - growth_mol - nuc_mol
    # Przyrost rozmiaru kryształu
    dddt = cryst_growth
    # Zmiana liczby kryształów
    dNdt = cryst_nuc 
    
    return [dCO2dt, dCaOHdt, dCaCO3dt, dddt, dNdt]