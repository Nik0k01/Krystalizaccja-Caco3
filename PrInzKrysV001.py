from scipy.integrate import solve_ivp
from model_SDR import model_SDR
from plotuj import plotuj

def main():  
    # Dane fizyczne; stała rozpuszczalności, stałe kinetyczne, współczynniki równań...
    dane_fiz = {'k_sp': 3.47e-3, 'k_g': 8.06e-9, 'k_rxn': 12.4, 'g': 2,
                'k_nuc': 1e7, 'n': 4.2, 'k_agg': 2.3}
    # Warunki panujące w układzie na początku symulacji oraz nasze założenia
    dane_init = {'c_caoh_0': (4 - 1.85) * 1e3 / 74.093, 'c_caoh_max': 1.85e3 / 74.093}
    
    # Czas obrotu dysku - np 120 obr/min
    t = 1 / (120 / 60) / 2
    
    # Maksymalna rozpuszczalność dwutlenku węgla 
    co2_sol_max = 0.0017e6 / 44
    # Całkowita ilość zasady wapniowej w układzie
    caoh_system = 4e3 / 74.093
    caco3_init = 0
    d_kryszt_init = 30e-9
    crystal_number = 0
    aggregate_number = 0
    
    y0 = [co2_sol_max, caoh_system, caco3_init, d_kryszt_init, crystal_number, aggregate_number]
    sol = solve_ivp(model_SDR, [0, t], y0, max_step=1e-2, args=(dane_init, dane_fiz))
    plotuj(sol, dane_init, dane_fiz)

if __name__ == "__main__":
    main()