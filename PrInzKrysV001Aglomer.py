import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

plt.style.reload_library()
plt.style.use('seaborn-v0_8')

# x = np.linspace(5e-9, 55e-9, 1000)
# y = norm.pdf(x, loc=30e-9, scale=8e-9)

dane_fiz = {'k_sp': 3.47e-3, 'k_g': 8.06e-9, 'k_rxn': 12.4, 'g': 2,
            'k_nuc': 1e7, 'n': 4.2, 'k_a': 2.3}
dane_init = {'c_caoh_0': (4 - 1.85)*1e3 / 74.093, 'd_cryst_init': 1e-8,
             'c_caoh_max': 1.85e3 / 74.093}

def model_SDR(t, y):
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
    
    # Szybkość aglomeracji
    lambda_s = y[2] ** 2 / dane_fiz['k_sp']
    l_1 = y[3]
    l_2 = y[3]
            
    # Stężenie CO2 utzrymywane na stałym poziomie
    dCO2dt = 0
    # Stężenie zasady 
    dCaOHdt = - k * y[0] * c_caoh_max if y[1] > c_caoh_max else - k * y[0] * y[1]
    # Stężenie węglanu
    dCaCO3dt = -dCaOHdt - cryst_growth - cryst_nuc
    
    # Przyrost rozmiaru kryształu
    dddt = cryst_growth * 2
    dNdt = cryst_nuc
    
    return [dCO2dt, dCaOHdt, dCaCO3dt, dddt, dNdt]
    
    
# Czas obrotu dysku - np 120 obr/min
t = 1 / (120 / 60) / 2
y0 = [0.0017e6 / 44, 4e3 / 74.093, 0, 30e-9, 0]
sol = solve_ivp(model_SDR, [0, t], y0, max_step=1e-6)


plt.figure(figsize=(10,6))
plt.plot(sol.t, sol.y[2])
plt.title(r'$\Delta$ $C_{CaCO3}$')
plt.xlabel('Czas [s]')
plt.ylabel('mol/m3')
plt.savefig('CaCo3.png')


plt.figure(figsize=(10,6))
plt.plot(sol.t, sol.y[3])
plt.title(r'$\Delta d_{kryszt}$')
plt.xlabel('czas [s]')
plt.ylabel('d [m]')
plt.savefig('Rozmiar.png')


plt.figure(figsize=(10,6))
plt.plot(x, y, 'r-')
plt.xlabel('L [m]')
plt.ylabel('x [-]')
plt.legend(['Rozkład przed krystalizacją', 'Rozkład po krystalizacji'])


plt.figure(figsize=(10,6))
plt.plot(sol.t, sol.y[4])
plt.title(r'$N_{kryszt}$')
plt.xlabel('czas [s]')
plt.ylabel('N [#/m3]')
plt.savefig('Liczba.png')

plt.figure(figsize=(10,6))
plt.plot(sol.t, sol.y[1])
plt.title(r'$\Delta$ $C_{Ca(OH)_2}$')
plt.xlabel('czas [s]')
plt.ylabel('mol/m3')
plt.savefig('CaOH.png')


s = ((sol.y[2] - dane_fiz['k_sp'] / dane_init['c_caoh_max']) /
    dane_fiz['k_sp'] / dane_init['c_caoh_max'])
# s[s < 0] = 0

plt.figure(figsize=(10,6))
plt.plot(sol.t, s)
plt.title('Przesycenie S')
plt.xlabel('czas [s]')
plt.ylabel('[-]')
plt.savefig('Przesycenie.png')
plt.show()
