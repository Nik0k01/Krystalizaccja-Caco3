import matplotlib.pyplot as plt
import numpy as np

plt.style.reload_library()
plt.style.use('bmh')

def plotuj(sol, dane_init, dane_fiz):
    """
    Ta fukcja przedstawia wyniki symulacji w sposób graficzny
    """
    
    plt.figure(figsize=(10,6))
    plt.plot(sol.t, sol.y[2])
    plt.title(r'$\Delta$ $C_{CaCO3}$')
    plt.xlabel('Czas [s]')
    plt.ylabel('mol/m3')
    plt.savefig('Wykresy/CaCo3.png')


    plt.figure(figsize=(10,6))
    plt.plot(sol.t, sol.y[3])
    plt.title(r'$\Delta d_{kryszt}$')
    plt.xlabel('czas [s]')
    plt.ylabel('d [m]')
    plt.savefig('Wykresy/Rozmiar.png')


    # plt.figure(figsize=(10,6))
    # plt.plot(x, y, 'r-',
    #          x_end, y, '--')
    # plt.xlabel('L [m]')
    # plt.ylabel('x [-]')
    # plt.legend(['Rozkład przed krystalizacją', 'Rozkład po krystalizacji'])


    plt.figure(figsize=(10,6))
    plt.plot(sol.t, sol.y[4])
    plt.title(r'$N_{kryszt}$')
    plt.xlabel('czas [s]')
    plt.ylabel('N [#/m3]')
    plt.savefig('Wykresy/Liczba.png')

    plt.figure(figsize=(10,6))
    plt.plot(sol.t, sol.y[1])
    plt.title(r'$\Delta$ $C_{Ca(OH)_2}$')
    plt.xlabel('czas [s]')
    plt.ylabel('mol/m3')
    plt.savefig('Wykresy/CaOH.png')


    a = np.where(sol.y[1] < dane_init['c_caoh_max'], sol.y[1], dane_init['c_caoh_max'])
    s = sol.y[2] ** 2 / dane_fiz['k_sp']
    # s[s < 0] = 0

    plt.figure(figsize=(10,6))
    plt.plot(sol.t, s)
    plt.title('Przesycenie S')
    plt.xlabel('czas [s]')
    plt.ylabel('[-]')
    plt.savefig('Wykresy/Przesycenie.png')
