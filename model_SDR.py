from aggreg_func import aggreg_func

def model_SDR(t, y, dane_init, dane_fiz):
    """
    Ta funkcja ma za zadanie zdefiniować układ równań różniczkowych zwyczajnych, opisujących
    krystalizację węglanu wapnia w reaktorze z obrotowymi dyskami
    """
    # 0 - CO2, 1 - Ca(OH)2, 2 - CaCO3
    c_caoh_max = dane_init['c_caoh_max']
    k = dane_fiz['k_rxn']
    n = dane_fiz['n']
    g = dane_fiz['g']
    c_satur = dane_fiz['k_sp'] / c_caoh_max
    
    # Szybkość wzrostu kryształu
    if (y[2] - c_satur) > 0:
        cryst_growth = dane_fiz['k_g'] * (y[2] - c_satur)**g
    else:
        cryst_growth = 0
        
    # Szybkość nukleacji 
    if (y[2] - c_satur) > 0:
        cryst_nuc = dane_fiz['k_nuc'] * (y[2] - c_satur)**n   
    else:
        cryst_nuc = 0
        
    s = y[2] ** 2 / dane_fiz['k_sp']

    if (y[4] > 0):
        agg_rate = aggreg_func(y[3], 3e-8, **{'n_0': y[4], 'n_L': y[5], 'lambda_s': s}) * 1e10
    else:
        agg_rate = 0
        
    # Stężenie CO2 utzrymywane na stałym poziomie
    dCO2dt = 0
    # Stężenie zasady 
    dCaOHdt = - k * y[0] * c_caoh_max if y[1] > c_caoh_max else - k * y[0] * y[1]
    # Stężenie węglanu
    dCaCO3dt = -dCaOHdt - cryst_growth - cryst_nuc
  
    
    # Przyrost rozmiaru kryształu
    dddt = cryst_growth * 2 + agg_rate * 2
    dNdt = cryst_nuc - agg_rate
    dAggdt = agg_rate
    
    return [dCO2dt, dCaOHdt, dCaCO3dt, dddt, dNdt, dAggdt]