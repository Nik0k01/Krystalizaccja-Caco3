from scipy.integrate import solve_ivp
from model_RDR import model_RDR
from plotuj import plotuj
from eksport_danych import eksport_danych


def main():  
    # Dane fizyczne; stała rozpuszczalności, stałe kinetyczne, współczynniki równań...
    dane_fiz = {'k_sp': 3.47e-3, 'k_g': 8.06e-9, 'k_rxn': 12.4, 'g': 2,
                'k_nuc': 1e7, 'n': 4.2, 'Na': 6.02e23,
                'crystal_density': 2710, 'molar_mass': 100.09}
    # Czas obrotu dysku - np 120 obr/min
    t = 0.25
    # Maksymalna rozpuszczalność dwutlenku węgla 
    co2_sol_max = 41.1 # mol/m3
    # Stężenie zasady wapniowej na początku w warstwece cieczy
    caoh_init = 22.5 # mol/m3
    caco3_init = 0
    d_kryszt_init = 30e-9 # m
    crystal_number = 0
    # Warunki panujące w układzie na początku symulacji oraz nasze założenia
    dane_init = {'d_init': d_kryszt_init, 'initial_distribution': (crystal_number, d_kryszt_init)}
    y0 = [co2_sol_max, caoh_init, caco3_init, d_kryszt_init, crystal_number]
    sol = solve_ivp(model_RDR, [0, t], y0, args=(dane_init, dane_fiz))
    # Sporządź wykresy
    plotuj(sol, dane_init, dane_fiz)
    # Eksportuj wyniki do arkusza kalkulacyjnego
    eksport_danych(sol)


if __name__ == "__main__":
    main()