import numpy as np
itmax = 100
itsm = 1e6

Na = 6.022e23 # Liczba Avogadro
cryst_den_mol = 2.710e6 / 100.087 # Molowa gęstość kryształu? mol/m3
k_rxn = 12.4 # Szybkość reakcji chemicznej m3/s/mol
k_nuc = 1e7 # Szybkość nukleacji homogenicznej mol^(3n-3)/s
k_growth = 8.06e-9 # Stała wzrostu - nie jest nigdzie używana w pliku?
co2_sol_max = 0.0017e6 / 44 # Rozpuszczalność CO2 w wodzie ~ 18 stopnii C mol/m3
gamm = k_rxn * co2_sol_max # maksymalna szybkość reakcji? Niepełne wyrażenie
k_sp = 3.47e-3 # stała rozpuszczalności CaCO3
d_cryst_init = 1e-8 # Średnica tworzących się zarodników - można se różnie założyć 
r_cryst_init = d_cryst_init / 2 # Jak wyżej tyle że promień
Vmn = 4 * np.pi * r_cryst_init**3 * Na # Objętość mola kryształów?
n = 4.2 # wykładnik przy prędkości zarodkowania
g = 2 # wykładnik przy prędkości wzrostu
# maksymlane stężenie wodorotlenku wapnia w roztworze - mol/m3
c_caoh_max = 1.85e3 / 74.093 
# Ilość (stężenie) wodorotlenku wapnia we wsadzie (reaktorze)
slurry = 4e3 / 74.093
# Stężenie wodorotlenku wapnia w roztworze
b0 = c_caoh_max
# Stężenie molowe stauracji - nie wiem po co skoro już wcześniej zdefinowane
# Może to jest potrzebne stężenie CO_3^2- do wytrącenia
csat = k_sp / c_caoh_max
# Pozostała ilość wodorotlenku wapnia w reaktorze
cslurry = slurry - b0
# Czas wyrażony stężeniem zasady wapniowej - coś względem maksymalnej szyb.
tslurry = cslurry / (k_rxn * co2_sol_max * b0)
# 21000 - czas prowadzenia procesu (350 min) - krok czasowy całkowania
dt = 21000 * csat / (k_rxn * co2_sol_max * b0)
t2 = 0
c2 = 0
Surf = 0

r = np.zeros(itmax)
rho = np.zeros(itmax)

cfree2 = 0
f = open('wyniki.txt', 'w')

for i in range(itmax):
    ddt = dt / itsm
    dr = 0
    
    for j in range(int(itsm)):
        t2 = i * dt + j * ddt
        c1 = c2
        c2 = k_rxn * co2_sol_max * b0 * t2
        if c2 > cslurry:
            c2 = cslurry + b0 * (1 - np.exp(-gamm * (t2 - tslurry)))
        
        dc = c2 - c1
        cfree1 = cfree2
        cfree2 = cfree1 + dc
        cfree = 0.5 * (cfree1 + cfree2)
        if (cfree > csat):
            ddrho = ddt * k_nuc * (cfree - csat)**n
            rho[i] = rho[i] + ddrho
            cfree2 = cfree2 - cryst_den_mol * Vmn * ddrho
            ddr = ddt * k_growth * (cfree - csat)**g
            cfree2 = cfree2 - cryst_den_mol * Surf * ddr
            dr = dr + ddr
    
    r[i] = r_cryst_init + dr / 2
    
    Vgrow = 0
    Surf = Na * rho[i] * 4 * np.pi * r_cryst_init**2 
    
    if i != 0:
        for k in range(i):
            Vgrow = Vgrow + rho[k] * Na * 4 * np.pi * dr * (r[k]**2 + 
                    r[k] * dr + dr**2 / 3)
            r[k] = r[k] + dr
            Surf = Surf + Na * rho[k] * 4 * np.pi * r[k] ** 2
        
    c_caoh_max = cfree2 + b0
    if (c2 > cslurry):
        c_caoh_max = cfree2 + b0 * np.exp(-gamm * (t2 - tslurry))
        
    csat = k_sp / c_caoh_max
    
    print(f'Iteracja: {i}', file=f)
    print(f't2 = {t2}, cfree = {cfree}', file=f)
    print('*****************************************', file=f)
    
    if i != 0:
        for k in range(i):
            print(f'rho[{k}] = {rho[k]}, 2 * r[{k}] = {r[k]}', file=f)
            

    
        

