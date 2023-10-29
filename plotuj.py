import matplotlib.pyplot as plt
import numpy as np

plt.style.reload_library()
plt.style.use('bmh')

def plotuj(sol, dane_init, dane_fiz):
    """
    Ta fukcja graficznie przedstawia wyniki symulacji
    """
    
    plt.figure(dpi=600, figsize=(6,4))
    plt.plot(sol.t, sol.y[2])
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$c_{CaCO_3}$ [mol/m$^3$]')
    plt.savefig('Wykresy/CaCo3.png')

    plt.figure(dpi=600, figsize=(6,4))
    plt.plot(sol.t, sol.y[3])
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$d$ [m]')
    plt.savefig('Wykresy/Rozmiar.png')

    plt.figure(dpi=600, figsize=(6,4))
    plt.plot(sol.t, sol.y[4])
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$N$ [#/m$^3$]')
    plt.savefig('Wykresy/Liczba.png')

    plt.figure(dpi=600, figsize=(6,4))
    plt.plot(sol.t, sol.y[1])
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$C_{Ca(OH)_2}$ [mol/m$^3$]')
    plt.savefig('Wykresy/CaOH.png')

    s = sol.y[2] - np.sqrt(dane_fiz['k_sp'])
    plt.figure(dpi=600, figsize=(6,4))
    plt.plot(sol.t, s)
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$S$ [mol/m$^3$]')
    plt.savefig('Wykresy/Przesycenie.png')
