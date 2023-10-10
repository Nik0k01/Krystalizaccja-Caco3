from scipy.integrate import solve_ivp
from model_SDR import model_SDR
from plotuj import plotuj
import xlwings as xw
import numpy as np

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
    
    y0 = [co2_sol_max, caoh_system, caco3_init, d_kryszt_init, crystal_number]
    sol = solve_ivp(model_SDR, [0, t], y0, args=(dane_init, dane_fiz))
    plotuj(sol, dane_init, dane_fiz)

    book = xw.Book('template.xltx')
    sheet = book.sheets[0]
    sheet['B3'].options(transpose=True).value = sol.t
    sheet['C3'].options(transpose=True).value = sol.y[0]
    sheet['D3'].options(transpose=True).value = sol.y[1]
    sheet['E3'].options(transpose=True).value = sol.y[2]
    sheet['F3'].options(transpose=True).value = sol.y[3]
    sheet['G3'].options(transpose=True).value = sol.y[4]
    book.save('Tabele_pliki_txt/Nukleacja.xlsx')
    book.close()

if __name__ == "__main__":
    main()