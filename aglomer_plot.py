import matplotlib.pyplot as plt
plt.style.use('bmh')

def aglomer_plot(crystal_array, crystal_number):
    plt.figure(dpi=600, figsize=(6,4))
    plt.hist(crystal_array, bins=7, rwidth=0.9)
    plt.xlabel("Rozmiar [nm]")
    plt.ylabel("Liczba kryształów [-]")
    plt.savefig("Wykresy/aglomeracja.png")

    iters = list(map(int, list(crystal_number.keys())))
    crystal_number = list(crystal_number.values())
    plt.figure(dpi=600, figsize=(6,4))
    plt.plot(iters, crystal_number)
    plt.xlabel("Iteracja")
    plt.ylabel("Całkowita liczba kryształów [-]")
    plt.savefig("Wykresy/l_kryst_aglomer_iter.png")